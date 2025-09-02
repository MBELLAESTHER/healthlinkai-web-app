from datetime import datetime, date
from models import db, UsageLog, Subscription
from flask import session, jsonify

# Freemium limits
USAGE_LIMITS = {
    'free': {
        'symptom_check': 5,  # 5 symptom checks per day
        'mindwell_chat': 10,  # 10 chat messages per day
        'provider_lookup': 3  # 3 provider lookups per day
    },
    'premium': {
        'symptom_check': float('inf'),  # Unlimited
        'mindwell_chat': float('inf'),  # Unlimited
        'provider_lookup': float('inf')  # Unlimited
    }
}

def get_user_subscription(user_id):
    """Get user's current subscription plan"""
    subscription = Subscription.query.filter_by(
        user_id=user_id, 
        status='active'
    ).first()
    
    if not subscription:
        # Create default free subscription
        subscription = Subscription(user_id=user_id, plan='free')
        db.session.add(subscription)
        db.session.commit()
    
    return subscription

def get_daily_usage(user_id, feature, target_date=None):
    """Get user's daily usage count for a specific feature"""
    if target_date is None:
        target_date = date.today()
    
    usage = UsageLog.query.filter_by(
        user_id=user_id,
        feature=feature,
        date=target_date
    ).first()
    
    return usage.count if usage else 0

def track_usage(user_id, feature):
    """Track usage for a feature and update/create usage log"""
    today = date.today()
    
    usage = UsageLog.query.filter_by(
        user_id=user_id,
        feature=feature,
        date=today
    ).first()
    
    if usage:
        usage.count += 1
    else:
        usage = UsageLog(
            user_id=user_id,
            feature=feature,
            date=today,
            count=1
        )
        db.session.add(usage)
    
    db.session.commit()
    return usage.count

def check_usage_limit(user_id, feature):
    """Check if user has exceeded their daily limit for a feature"""
    subscription = get_user_subscription(user_id)
    current_usage = get_daily_usage(user_id, feature)
    limit = USAGE_LIMITS[subscription.plan][feature]
    
    return {
        'allowed': current_usage < limit,
        'current': current_usage,
        'limit': limit if limit != float('inf') else 'Unlimited',
        'plan': subscription.plan,
        'remaining': max(0, limit - current_usage) if limit != float('inf') else 'Unlimited'
    }

def require_usage_limit(user_id, feature):
    """Decorator-like function to check usage limits before allowing access"""
    usage_check = check_usage_limit(user_id, feature)
    
    if not usage_check['allowed']:
        return {
            'error': 'Usage limit exceeded',
            'message': f"You've reached your daily limit of {usage_check['limit']} {feature.replace('_', ' ')}s. Upgrade to Premium for unlimited access!",
            'current_plan': usage_check['plan'],
            'upgrade_required': True
        }
    
    # Track the usage
    track_usage(user_id, feature)
    return {'success': True}

def get_usage_summary(user_id):
    """Get comprehensive usage summary for dashboard"""
    subscription = get_user_subscription(user_id)
    today = date.today()
    
    summary = {
        'plan': subscription.plan,
        'features': {}
    }
    
    for feature in ['symptom_check', 'mindwell_chat', 'provider_lookup']:
        current = get_daily_usage(user_id, feature, today)
        limit = USAGE_LIMITS[subscription.plan][feature]
        
        summary['features'][feature] = {
            'current': current,
            'limit': limit if limit != float('inf') else 'Unlimited',
            'remaining': max(0, limit - current) if limit != float('inf') else 'Unlimited',
            'percentage': (current / limit * 100) if limit != float('inf') else 0
        }
    
    return summary
