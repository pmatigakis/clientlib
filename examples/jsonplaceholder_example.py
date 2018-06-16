from collections import namedtuple

from marshmallow import Schema, post_load, fields

from clientlib.endpoints import Endpoint
from clientlib.clients import Client


Post = namedtuple("Post", ["userId", "id", "title", "body"])
NewPost = namedtuple("NewPost", ["title", "body"])
CreatedPost = namedtuple("CreatedPost", ["id", "title", "body"])


class PostSchema(Schema):
    userId = fields.Int(required=True)
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)

    @post_load
    def make_post(self, data):
        return Post(**data)


class NewPostSchema(Schema):
    title = fields.Str(required=True)
    body = fields.Str(required=True)


class CreatedPostSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)

    @post_load
    def make_created_post(self, data):
        return CreatedPost(**data)


class JsonPlaceholder(Client):
    post = Endpoint(
        method="GET",
        endpoint="/posts/{post_id}",
        args=["post_id"],
        response_schema=PostSchema()
    )

    posts = Endpoint(
        method="GET",
        endpoint="/posts",
        response_schema=PostSchema(many=True)
    )

    create_post = Endpoint(
        method="POST",
        endpoint="/posts",
        response_schema=CreatedPostSchema(),
        payload_schema=NewPostSchema(),
        payload="post"
    )


def main():
    client = JsonPlaceholder(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=5
    )

    # get the contents of a post
    response = client.post(post_id=1)
    # the response.data attribute contains a Post instance
    print(response.data)

    # get a list of posts
    response = client.posts()
    # the response.data attribute contains a list of Post objects
    print("number of posts: {}".format(len(response.data)))
    print(response.data[0])

    # create a post
    post = NewPost(title="my post", body="my post contents")
    response = client.create_post(post=post)
    # the response.data attribute contains a CreatedPost object
    print(response.data)


if __name__ == "__main__":
    main()
