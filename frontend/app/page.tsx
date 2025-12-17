"use client"; // This marks this as a Client Component (interactive)

import { useState, useEffect } from 'react';

// Define what a Post looks like (matching Python Pydantic model)
interface Post {
  id: string;
  title: string;
  content: string;
  video_url: string;
  created_at: string;
  likes: number;
}

export default function Home() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [form, setForm] = useState({ title: '', content: '', video_url: '' });
  const [loading, setLoading] = useState(false);

  // 1. Fetch Posts on Load (US-2)
  useEffect(() => {
    fetch('http://127.0.0.1:8000/posts')
      .then((res) => res.json())
      .then((data) => setPosts(data))
      .catch((err) => console.error("Failed to fetch posts:", err));
  }, []);

  // 2. Handle Create Post (US-1)
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
        const newPost = await res.json();
        setPosts([newPost, ...posts]); // Add new post to top of list
        setForm({ title: '', content: '', video_url: '' }); // Clear form
      }
    } catch (error) {
      console.error("Error creating post:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gray-50 text-gray-800">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-center text-blue-600">DailyLog Vlog</h1>

        {/* --- US-1: Create Post Form --- */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-semibold mb-4">Share your day</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="Title (e.g., Morning Coffee)"
              className="w-full p-2 border rounded"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              required
            />
            <textarea
              placeholder="How was your day?"
              className="w-full p-2 border rounded"
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
              required
            />
            <input
              type="url"
              placeholder="Video URL (YouTube link)"
              className="w-full p-2 border rounded"
              value={form.video_url}
              onChange={(e) => setForm({ ...form, video_url: e.target.value })}
              required
            />
            <button 
              type="submit" 
              disabled={loading}
              className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Posting...' : 'Post Vlog'}
            </button>
          </form>
        </div>

        {/* --- US-2: List Posts --- */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold">Recent Vlogs</h2>
          {posts.map((post) => (
            <div key={post.id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="flex justify-between items-start">
                <h3 className="text-lg font-bold">{post.title}</h3>
                <span className="text-xs text-gray-500">
                  {new Date(post.created_at).toLocaleDateString()}
                </span>
              </div>
              <p className="text-gray-600 mt-2 mb-4">{post.content}</p>
              <a 
                href={post.video_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-500 underline text-sm"
              >
                Watch Video &rarr;
              </a>
            </div>
          ))}
          {posts.length === 0 && <p className="text-center text-gray-500">No vlogs yet. Be the first!</p>}
        </div>
      </div>
    </main>
  );
}