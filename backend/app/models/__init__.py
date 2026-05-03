from sqlalchemy import Column, String, UUID, DateTime, Boolean, Enum, Integer, Text, Float, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum as PyEnum
import uuid

Base = declarative_base()

# Enums
class UserRole(str, PyEnum):
    ATHLETE = "ATHLETE"
    COACH = "COACH"
    RECRUITER = "RECRUITER"
    NGO = "NGO"
    SPONSOR = "SPONSOR"

class SkillLevel(str, PyEnum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    PROFESSIONAL = "PROFESSIONAL"

class Visibility(str, PyEnum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    FOLLOWERS_ONLY = "FOLLOWERS_ONLY"

class ConnectionStatus(str, PyEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    BLOCKED = "BLOCKED"

class LikeType(str, PyEnum):
    LIKE = "LIKE"
    LOVE = "LOVE"
    CELEBRATE = "CELEBRATE"
    SUPPORT = "SUPPORT"

class NotificationType(str, PyEnum):
    LIKE = "LIKE"
    COMMENT = "COMMENT"
    FOLLOW = "FOLLOW"
    MENTION = "MENTION"
    MESSAGE = "MESSAGE"
    TALENT_ALERT = "TALENT_ALERT"
    CONNECTION_REQUEST = "CONNECTION_REQUEST"
    ACHIEVEMENT = "ACHIEVEMENT"

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(Enum(UserRole), nullable=False, index=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    profile_picture_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    bio = Column(Text)
    location = Column(String(255), index=True)
    sport = Column(String(100), nullable=False, index=True)
    skill_level = Column(Enum(SkillLevel), default=SkillLevel.BEGINNER, index=True)
    achievements = Column(ARRAY(String))
    stats = Column(JSON)
    connections_count = Column(Integer, default=0)
    followers_count = Column(Integer, default=0)
    followers_following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    reels_count = Column(Integer, default=0)
    website_url = Column(String(255))
    phone_number = Column(String(20))
    birth_date = Column(DateTime)
    gender = Column(String(20))
    verification_badge = Column(Boolean, default=False)
    badge_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    title = Column(String(255))
    content = Column(Text, nullable=False)
    image_urls = Column(ARRAY(String))
    video_url = Column(String(500))
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    visibility = Column(Enum(Visibility), default=Visibility.PUBLIC, index=True)
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Reel(Base):
    __tablename__ = "reels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    title = Column(String(255))
    description = Column(Text)
    video_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    duration = Column(Integer)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0, index=True)
    sport = Column(String(100), index=True)
    tags = Column(ARRAY(String))
    visibility = Column(Enum(Visibility), default=Visibility.PUBLIC)
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    post_id = Column(UUID(as_uuid=True), index=True)
    reel_id = Column(UUID(as_uuid=True), index=True)
    parent_comment_id = Column(UUID(as_uuid=True))
    content = Column(Text, nullable=False)
    likes_count = Column(Integer, default=0)
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    post_id = Column(UUID(as_uuid=True), index=True)
    reel_id = Column(UUID(as_uuid=True), index=True)
    comment_id = Column(UUID(as_uuid=True), index=True)
    like_type = Column(Enum(LikeType), default=LikeType.LIKE)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Connection(Base):
    __tablename__ = "connections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    follower_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    following_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    status = Column(Enum(ConnectionStatus), default=ConnectionStatus.ACCEPTED, index=True)
    connection_type = Column(String(50), default="FOLLOW")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    accepted_at = Column(DateTime)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    recipient_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="TEXT")
    media_url = Column(String(500))
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    actor_id = Column(UUID(as_uuid=True))
    notification_type = Column(Enum(NotificationType), nullable=False, index=True)
    related_post_id = Column(UUID(as_uuid=True))
    related_reel_id = Column(UUID(as_uuid=True))
    related_user_id = Column(UUID(as_uuid=True))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    metric_type = Column(String(100), nullable=False)
    metric_value = Column(JSON, nullable=False)
    sport = Column(String(100), index=True)
    date = Column(DateTime, nullable=False, index=True)
    engagement_score = Column(Integer, default=0, index=True)
    performance_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VerificationBadge(Base):
    __tablename__ = "verification_badges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    badge_type = Column(String(100), nullable=False)
    verification_date = Column(DateTime)
    expiry_date = Column(DateTime)
    verified_by_admin = Column(UUID(as_uuid=True))
    reason = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    recommended_user_id = Column(UUID(as_uuid=True), nullable=False)
    recommendation_type = Column(String(50), nullable=False)
    score = Column(Float, default=0)
    reason = Column(Text)
    is_accepted = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class TalentAlert(Base):
    __tablename__ = "talent_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    ngo_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    alert_type = Column(String(100), nullable=False)
    trigger_metric = Column(JSON, nullable=False)
    message = Column(Text)
    is_read = Column(Boolean, default=False, index=True)
    is_actioned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
