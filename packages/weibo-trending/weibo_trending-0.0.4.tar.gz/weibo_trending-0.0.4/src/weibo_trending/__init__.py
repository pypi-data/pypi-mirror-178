from dataclasses import dataclass, asdict
from typing import List, Optional

import requests
from bs4 import BeautifulSoup, Tag

request_url = "https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0"
request_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "MWeibo-Pwa": "1",
    "Connection": "keep-alive",
    "Referer": "https://m.weibo.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "TE": "trailers",
}


def get_new_posts() -> dict:
    """Get new posts from Weibo, and return the rawo JSON response.
    A successful response contains 10 new posts.
    """
    resp = requests.get(url=request_url, headers=request_headers)
    resp.raise_for_status()
    return resp.json()


@dataclass
class User:
    id: int
    profile_url: str
    screen_name: str
    gender: str
    followers_count: str  # Example: "433.8万".


@dataclass
class Microblog:
    text: str
    id: str
    url: str
    poster: User
    pics: List[str]
    created_at: str
    source: str  # `source` is the device used to create the microblog.

    def to_dict(self) -> dict:
        return asdict(self)


def parse_mblog(mblog: dict) -> Microblog:
    """Parse one mblog item."""
    user = User(
        id=mblog.get("user", {}).get("id", -1),
        screen_name=mblog.get("user", {}).get("screen_name", ""),
        profile_url=mblog.get("user", {}).get("profile_url", ""),
        gender=mblog.get("user", {}).get("gender", "?"),
        followers_count=mblog.get("user", {}).get("followers_count", ""),
    )

    # Extract pic URLs, if any.
    pics: List[str] = []
    if mblog.get("pic_num", 0) != 0:
        for pic_obj in mblog.get("pics", [{}]):
            if type(pic_obj) is str:
                continue
            pic_url = pic_obj.get("url", "")
            if pic_url:
                pics.append(pic_url.replace("orj360", "large"))

    return Microblog(
        id=mblog.get("id", ""),
        created_at=mblog.get("created_at", ""),
        text=mblog.get("text", ""),  # May contain HTML elements like anchor tags.
        source=mblog.get("source", ""),
        poster=user,
        url=f"https://m.weibo.cn/status/{mblog['id']}",
        pics=pics,
    )


def get_full_text_from_snippet(mb: Microblog) -> str:
    """Check if a Microblog's text is a snippet. If it is, get the full text."""
    # A snippet has a clickable "全文" anchor element at the end. Clicking on it
    # leads to the full post.
    soup = BeautifulSoup(mb.text, "lxml")
    anchors: List[Tag] = soup.find_all("a")
    if anchors:
        a = anchors[-1]
        href = a.get("href", "")
        if a.text == "全文" and href == f"/status/{mb.id}":
            # Get full text.
            u = f"https://m.weibo.cn/statuses/extend?id={mb.id}"
            h = request_headers.copy()
            h["Referer"] = f"https://m.weibo.cn/detail/{mb.id}"
            r = requests.get(u, headers=h)
            r.raise_for_status()
            s = BeautifulSoup(r.content, "lxml")
            return s.text
    return soup.text


def parse_response(data: dict) -> List[Microblog]:
    """Parse the raw JSON response from Weibo."""
    mblogs: List[Microblog] = []
    for card in data["data"]["cards"]:
        mb: Optional[dict] = card["mblog"]
        if not mb:
            continue

        u = mb.get("user")
        if u is None:
            # Post has been deleted.
            continue

        mblog = parse_mblog(mb)
        mblog.text = get_full_text_from_snippet(mblog)
        mblogs.append(mblog)
    return mblogs


@dataclass
class Comment:
    created_at: str
    id: str
    rootid: str  # The parent comment's ID.
    floor_number: int
    text: str
    source: str
    user: User
    comments: List["Comment"]  # Replies to this comment.
    isLikedByMblogAuthor: bool
    pic: str  # A comment can have only 1 pic.
    like_count: int


def get_raw_comments(post_id: str) -> List[dict]:
    url = (
        "https://m.weibo.cn/comments/"
        f"hotflow?id={post_id}&mid={post_id}&max_id_type=0"
    )
    h = request_headers.copy()
    h["Referer"] = f"https://m.weibo.cn/detail/{post_id}"
    r = requests.get(url, headers=h)
    r.raise_for_status()
    data: dict = r.json()

    raw_comments: List[dict] = data.get("data", {}).get("data", [])
    return raw_comments


def parse_comments(raw_comments: List[dict]) -> List[Comment]:
    """Parse all comments, include replies."""
    comments: List[Comment] = []
    for rc in raw_comments:
        u: dict = rc.get("user", {})
        user = User(
            id=u.get("id", -1),
            profile_url=u.get("profile_url", ""),
            screen_name=u.get("screen_name", ""),
            gender=u.get("gender", ""),
            followers_count=u.get("followers_count", ""),
        )

        # Extract nested comments. "comments" field could be `False`.
        nested_comments: List[dict] = (
            [] if not rc.get("comments") else rc.get("comments", [])
        )
        replies = parse_comments(nested_comments)

        # Extract pic URL, if any. Unlike front page data, a comment has only
        # one pic.
        pic_url: str = rc.get("pic", {}).get("large", {}).get("url", "")

        c = Comment(
            created_at=rc.get("created_at", ""),
            id=rc.get("id", ""),
            rootid=rc.get("rootid", ""),
            floor_number=rc.get("floor_number", -1),
            text=BeautifulSoup(rc.get("text", ""), "lxml").text,
            source=rc.get("source", ""),
            user=user,
            comments=replies,
            isLikedByMblogAuthor=rc.get("isLikedByMblogAuthor", False),
            pic=pic_url,
            like_count=rc.get("like_count", -1),
        )
        comments.append(c)
    return comments
