#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_platform.settings')
django.setup()

from users.models import User

# Delete old admin users
User.objects.filter(username__in=['admin', 'ismailovvibe']).delete()
print("✅ Old admin user(s) deleted")

# Create new admin user
new_admin = User.objects.create_superuser(
    username='ismailovvibe',
    email='admin@example.com',
    password='Jasurbek.314'
)
print("\n✅ New admin user created successfully!")
print("\n📋 NEW CREDENTIALS:")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📱 Username: ismailovvibe")
print("🔐 Password: Jasurbek.314")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("\n🔗 Admin URL: http://localhost:8000/admin/")
