"use client";

import { useState, useEffect } from 'react';

// Updated Types (match the Python models)
interface Comment {
  id: string;
  content: string;
  created_at: string;
}

interface Post {
  id: string;
  title: string;
  content: string;
  video_url: string;
  created_at: string;
  likes: number;
  comments: Comment[]; // Nested comments
}

export default function Home() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [form, setForm] = useState({ title: '', content: '', video_url: '' });
  const [commentInputs, setCommentInputs] = useState<{ [key: string]: string }>({}); // Track input per post
  const [loading, setLoading] = useState(false);

  // Fetch Posts
  const fetchPosts = () => {
    fetch('http://127.0.0.1:8000/posts')
      .then((res) => res.json())
      .then((data) => setPosts(data))
      .catch((err) => console.error("Failed to fetch posts:", err));
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  // Handle Create Post
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        fetchPosts(); // Refresh list
        setForm({ title: '', content: '', video_url: '' });
      }
    } catch (error) {
      console.error("Error creating post:", error);
    } finally {
      setLoading(false);
    }
  };

  // Handle Like
  const handleLike = async (postId: string) => {
    await fetch(`http://127.0.0.1:8000/posts/${postId}/like`, { method: 'POST' });
    fetchPosts(); // Refresh to see new count
  };

  // Handle Submit Comment (US-5)
  const handleCommentSubmit = async (postId: string) => {
    const content = commentInputs[postId];
    if (!content) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/posts/${postId}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      });

      if (res.ok) {
        setCommentInputs({ ...commentInputs, [postId]: '' }); // Clear input
        fetchPosts(); // Refresh to see new comment
      }
    } catch (error) {
      console.error("Error posting comment:", error);
    }
  };


  // US-6: Handle Delete Post
  const handleDeletePost = async (postId: string) => {
    if (!confirm("Are you sure you want to delete this vlog? This cannot be undone.")) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/posts/${postId}`, {
        method: 'DELETE',
      });
      if (res.ok) {
        // Remove from UI immediately
        setPosts(posts.filter((p) => p.id !== postId));
      }
    } catch (error) {
      console.error("Error deleting post:", error);
    }
  };

  // US-6: Handle Delete Comment
  const handleDeleteComment = async (postId: string, commentId: string) => {
    if (!confirm("Delete this comment?")) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/comments/${commentId}`, {
        method: 'DELETE',
      });
      if (res.ok) {
        // Update the UI by removing the comment from the specific post
        setPosts(posts.map(p => {
            if (p.id === postId) {
                return { ...p, comments: p.comments.filter(c => c.id !== commentId) };
            }
            return p;
        }));
      }
    } catch (error) {
      console.error("Error deleting comment:", error);
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gray-50 text-gray-800">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-center text-blue-600">DailyLog Vlog</h1>

        {/* Create Post Form */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-semibold mb-4">Share your day</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="Title"
              className="w-full p-2 border rounded"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              required
            />
            <textarea
              placeholder="Content"
              className="w-full p-2 border rounded"
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
              required
            />
            <input
              type="url"
              placeholder="Video URL"
              className="w-full p-2 border rounded"
              value={form.video_url}
              onChange={(e) => setForm({ ...form, video_url: e.target.value })}
              required
            />
            <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
              {loading ? 'Posting...' : 'Post Vlog'}
            </button>
          </form>
        </div>

        {/* Post List */}
        <div className="space-y-8">
          {posts.map((post) => (
            <div key={post.id} className="bg-white p-6 rounded-lg shadow relative group">
              <h3 className="text-xl font-bold">{post.title}</h3>
              <p className="text-gray-600 mb-2">{post.content}</p>
              <a href={post.video_url} target="_blank" className="text-blue-500 underline text-sm">Watch Video</a>

              {/* Like Section */}
              <div className="mt-4 flex items-center space-x-2">
                <button onClick={() => handleLike(post.id)} className="text-red-500 hover:text-red-700">
                  ❤️ {post.likes} Likes
                </button>
              </div>

              {/* DELETE POST BUTTON (Top Right) */}
              <button 
                onClick={() => handleDeletePost(post.id)}
                className="absolute top-4 right-4 text-gray-300 hover:text-red-600 transition"
                title="Delete Post"
              >
                🗑️
              </button>

              {/* Comments Section (US-5) */}
              <div className="mt-6 border-t pt-4">
                <h4 className="font-semibold mb-2">Comments</h4>
                <div className="space-y-2 mb-4">
                  {post.comments.map((comment) => (
                    <div key={comment.id} className="bg-gray-100 p-2 rounded text-sm flex justify-between items-start group">
                      {comment.content}
                      {/* DELETE COMMENT BUTTON */}
                      <button 
                        onClick={() => handleDeleteComment(post.id, comment.id)}
                        className="text-gray-400 hover:text-red-500 ml-2 opacity-0 group-hover:opacity-100 transition"
                        title="Delete Comment"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                  {post.comments.length === 0 && <p className="text-sm text-gray-400">No comments yet.</p>}
                </div>
                
                {/* Comment Input */}
                <div className="flex gap-2">
                  <input 
                    type="text" 
                    placeholder="Write a comment..." 
                    className="flex-1 p-2 border rounded text-sm"
                    value={commentInputs[post.id] || ''}
                    onChange={(e) => setCommentInputs({ ...commentInputs, [post.id]: e.target.value })}
                  />
                  <button 
                    onClick={() => handleCommentSubmit(post.id)}
                    className="bg-gray-200 px-4 py-2 rounded text-sm hover:bg-gray-300"
                  >
                    Reply
                  </button>
                </div>
              </div>

            </div>
          ))}
        </div>
      </div>
    </main>
  );
}