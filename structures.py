from typing import NamedTuple


class PostTproger(NamedTuple):
    href: str
    title: str
    text: str
    key: str


class PostHabr(NamedTuple):
    title: str
    href: str
    tags: str
    text: str
    key: str


class PostCrackWatch(NamedTuple):
    title: str
    protections: str
    groups: str
    releaseDate: str
    image: str
    crackDate: str
    href: str
    key: str


class PostStopGame(NamedTuple):
    poster: str
    text: str
    score: str
    title: str
    href: str
