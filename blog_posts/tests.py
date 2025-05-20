from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import BlogPost, Comment

class BlogPostAPITests(APITestCase):
    def setUp(self):
        # create one post to play with
        self.existing = BlogPost.objects.create(
            title="Existing", content="Foo", author="Alice"
        )
        self.list_url   = reverse('post-list')
        self.create_url = reverse('post-create')
        self.detail_url = lambda pk: reverse('post-detail', kwargs={'pk': pk})

    def test_create_post(self):
        data = {
            "title": "New Post",
            "content": "Some content",
            "author": "Bob",
            "category": BlogPost.Categories.OTHER,
        }
        resp = self.client.post(self.create_url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 2)
        self.assertEqual(resp.data['title'], data['title'])

    def test_list_posts(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # if you’re using pagination, expect a “results” key:
        if 'results' in resp.data:
            self.assertIn('count', resp.data)
            self.assertIsInstance(resp.data['results'], list)
        else:
            self.assertIsInstance(resp.data, list)

    def test_update_and_delete_any_post(self):
        # Update the existing post (no auth required)
        update_data = {
            "title": "Changed",
            "content": "Bar",
            "author": "Charlie",
            "category": BlogPost.Categories.TECHNOLOGY,
        }
        resp = self.client.put(self.detail_url(self.existing.pk), update_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.existing.refresh_from_db()
        self.assertEqual(self.existing.title, "Changed")

        # Delete the existing post
        resp = self.client.delete(self.detail_url(self.existing.pk))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BlogPost.objects.filter(pk=self.existing.pk).exists())


class CommentAPITests(APITestCase):
    def setUp(self):
        self.post = BlogPost.objects.create(
            title="Post", content="X", author="Alice"
        )
        self.create_url = reverse('comment-create', kwargs={'post_id': self.post.pk})
        self.detail_url = lambda cid: reverse(
            'comment-detail',
            kwargs={'post_id': self.post.pk, 'comment_id': cid}
        )

    def test_create_comment(self):
        data = {
            "content": "Nice post!",
            "author": "Dave"
        }
        resp = self.client.post(self.create_url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(resp.data['author'], "Dave")

    def test_update_and_delete_any_comment(self):
        comment = Comment.objects.create(post=self.post, content="Hi", author="Eve")
        # update
        update_data = {"content": "Updated", "author": "Frank"}
        resp = self.client.put(self.detail_url(comment.pk), update_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.content, "Updated")
        # delete
        resp = self.client.delete(self.detail_url(comment.pk))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())


class PaginationTests(APITestCase):
    def setUp(self):
        # create 15 posts to test pagination
        for i in range(15):
            BlogPost.objects.create(
                title=f"Post {i}", content="c", author="Auth"
            )
        self.list_url = reverse('post-list')

    def test_default_pagination(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # expecting DRF-style pagination
        self.assertIn('count', resp.data)
        self.assertIn('results', resp.data)
        self.assertEqual(resp.data['count'], 15)
        self.assertEqual(len(resp.data['results']), 10)  # default page_size=10

    def test_custom_page_size(self):
        resp = self.client.get(self.list_url + '?page_size=5')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['results']), 5)
