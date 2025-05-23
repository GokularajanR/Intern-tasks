from database.postgres_connector import create_session, Post, User

async def create_post(title: str, content: str, username: str):
    session = create_session()
    post = Post(title=title, content=content, created_by=username)
    session.add(post)
    session.commit()
    return post


async def get_all_posts():
    session = create_session()
    return session.query(Post).all()


async def get_post_by_id(post_id: int):
    session = create_session()
    post = session.query(Post).get(post_id)
    if not post:
        raise ValueError("Post not found.")
    return post


async def update_post(post_id: int, title: str, content: str):
    session = create_session()
    post = session.query(Post).get(post_id)
    if not post:
        raise ValueError("Post not found.")

    post.title = title
    post.content = content
    session.commit()
    return post


async def delete_post(post_id: int):
    session = create_session()
    post = session.query(Post).get(post_id)
    if not post:
        raise ValueError("Post not found.")

    session.delete(post)
    session.commit()
    return True