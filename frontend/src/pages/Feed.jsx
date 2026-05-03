import React, { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import "../styles/Feed.css";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

const Feed = () => {
  const [feed, setFeed] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [contentType, setContentType] = useState("all"); // all, posts, reels
  const [userLikes, setUserLikes] = useState({});

  const observerTarget = useRef(null);
  const pageSize = 10;

  // Get auth token
  const getAuthToken = () => localStorage.getItem("access_token");

  // Fetch feed data
  const fetchFeed = useCallback(
    async (pageNum) => {
      setLoading(true);
      setError("");

      try {
        const token = getAuthToken();
        const contentTypeParam =
          contentType === "all" ? "" : `&content_type=${contentType}`;

        const response = await axios.get(
          `${API_BASE_URL}/feed?page=${pageNum}&page_size=${pageSize}${contentTypeParam}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const newPosts = response.data.data || [];

        if (pageNum === 1) {
          setFeed(newPosts);
        } else {
          setFeed((prev) => [...prev, ...newPosts]);
        }

        setHasMore(response.data.has_next || false);
      } catch (err) {
        setError("Failed to load feed");
        console.error(err);
      } finally {
        setLoading(false);
      }
    },
    [contentType, pageSize]
  );

  // Initial load
  useEffect(() => {
    setPage(1);
    fetchFeed(1);
  }, [contentType]);

  // Infinite scroll observer
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loading) {
          const nextPage = page + 1;
          setPage(nextPage);
          fetchFeed(nextPage);
        }
      },
      { threshold: 0.1 }
    );

    if (observerTarget.current) {
      observer.observe(observerTarget.current);
    }

    return () => {
      if (observerTarget.current) {
        observer.unobserve(observerTarget.current);
      }
    };
  }, [page, hasMore, loading, fetchFeed]);

  // Handle like
  const handleLike = async (postId, likeType = "LIKE") => {
    try {
      const token = getAuthToken();
      const likeKey = `${postId}-${likeType}`;

      if (userLikes[likeKey]) {
        // Unlike
        await axios.delete(
          `${API_BASE_URL}/posts/${postId}/likes/${userLikes[likeKey]}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        setUserLikes((prev) => {
          const updated = { ...prev };
          delete updated[likeKey];
          return updated;
        });
      } else {
        // Like
        const response = await axios.post(
          `${API_BASE_URL}/posts/${postId}/likes`,
          { like_type: likeType },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        setUserLikes((prev) => ({
          ...prev,
          [likeKey]: response.data.id,
        }));
      }

      // Update UI
      setFeed((prev) =>
        prev.map((post) => {
          if (post.id === postId) {
            return {
              ...post,
              likes_count: userLikes[likeKey]
                ? post.likes_count - 1
                : post.likes_count + 1,
            };
          }
          return post;
        })
      );
    } catch (err) {
      console.error("Failed to like post:", err);
    }
  };

  // Render post item
  const renderPostItem = (item) => {
    const isReel = item.video_url && !item.post_id;

    return (
      <div key={item.id} className="feed-item">
        {/* Author Info */}
        <div className="post-header">
          <div className="author-info">
            <img
              src={item.user?.profile_picture_url || "/default-avatar.png"}
              alt={item.user?.username}
              className="author-avatar"
            />
            <div className="author-details">
              <h3>{item.author_name || item.user?.username}</h3>
              <p>{new Date(item.created_at).toLocaleDateString()}</p>
            </div>
          </div>
          <button className="menu-btn">⋮</button>
        </div>

        {/* Content */}
        <div className="post-content">
          {item.title && <h2>{item.title}</h2>}
          <p>{item.content || item.description}</p>
        </div>

        {/* Media */}
        {item.image_urls && item.image_urls.length > 0 && (
          <div className="post-media">
            <div className="image-gallery">
              {item.image_urls.map((url, idx) => (
                <img
                  key={idx}
                  src={url}
                  alt={`Post image ${idx + 1}`}
                  className="post-image"
                />
              ))}
            </div>
          </div>
        )}

        {isReel && (
          <div className="reel-container">
            <video
              src={item.video_url}
              className="reel-video"
              controls
              controlsList="nodownload"
            />
            {item.duration && (
              <span className="reel-duration">
                {Math.floor(item.duration / 60)}:{(item.duration % 60)
                  .toString()
                  .padStart(2, "0")}
              </span>
            )}
          </div>
        )}

        {item.video_url && !isReel && (
          <div className="post-media">
            <video
              src={item.video_url}
              className="post-video"
              controls
              controlsList="nodownload"
            />
          </div>
        )}

        {/* Tags */}
        {item.tags && item.tags.length > 0 && (
          <div className="post-tags">
            {item.tags.map((tag) => (
              <span key={tag} className="tag">
                #{tag}
              </span>
            ))}
          </div>
        )}

        {/* Engagement Stats */}
        <div className="post-stats">
          <span>{item.likes_count} likes</span>
          <span>{item.comments_count} comments</span>
          <span>{item.shares_count} shares</span>
          {item.views_count && <span>{item.views_count} views</span>}
        </div>

        {/* Actions */}
        <div className="post-actions">
          <button
            className={`action-btn like-btn ${
              userLikes[`${item.id}-LIKE`] ? "active" : ""
            }`}
            onClick={() => handleLike(item.id, "LIKE")}
          >
            👍 Like
          </button>
          <button className="action-btn">💬 Comment</button>
          <button className="action-btn">❤️ Love</button>
          <button className="action-btn">🎉 Celebrate</button>
          <button className="action-btn">🤝 Support</button>
          <button className="action-btn">↗️ Share</button>
        </div>
      </div>
    );
  };

  return (
    <div className="feed-container">
      {/* Header */}
      <div className="feed-header">
        <h1>SportLink Feed</h1>
        <div className="filter-tabs">
          <button
            className={`tab ${contentType === "all" ? "active" : ""}`}
            onClick={() => setContentType("all")}
          >
            All
          </button>
          <button
            className={`tab ${contentType === "posts" ? "active" : ""}`}
            onClick={() => setContentType("posts")}
          >
            Posts
          </button>
          <button
            className={`tab ${contentType === "reels" ? "active" : ""}`}
            onClick={() => setContentType("reels")}
          >
            Reels
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && <div className="error-banner">{error}</div>}

      {/* Feed List */}
      <div className="feed-list">
        {feed.length === 0 && !loading && (
          <div className="empty-state">
            <p>No posts yet. Follow some users to see their posts!</p>
          </div>
        )}

        {feed.map((item) => renderPostItem(item))}

        {/* Loading Indicator */}
        {loading && (
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Loading more posts...</p>
          </div>
        )}

        {/* Infinite Scroll Target */}
        <div ref={observerTarget} className="observer-target" />

        {/* No More Posts */}
        {!hasMore && feed.length > 0 && (
          <div className="end-message">
            <p>You've reached the end of the feed</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Feed;
