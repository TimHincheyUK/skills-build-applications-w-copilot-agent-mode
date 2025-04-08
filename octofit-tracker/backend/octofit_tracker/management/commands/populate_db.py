from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data by directly interacting with the database
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM octofit_tracker_user")
            cursor.execute("DELETE FROM octofit_tracker_team")
            cursor.execute("DELETE FROM octofit_tracker_activity")
            cursor.execute("DELETE FROM octofit_tracker_leaderboard")
            cursor.execute("DELETE FROM octofit_tracker_workout")

        # Ensure all IDs are explicitly set as integers
        users = [
            User(id=1, email='thundergod@mhigh.edu', name='Thor', age=30, team='Blue Team'),
            User(id=2, email='metalgeek@mhigh.edu', name='Tony Stark', age=35, team='Gold Team'),
            User(id=3, email='zerocool@mhigh.edu', name='Steve Rogers', age=32, team='Blue Team'),
            User(id=4, email='crashoverride@mhigh.edu', name='Natasha Romanoff', age=28, team='Gold Team'),
            User(id=5, email='sleeptoken@mhigh.edu', name='Bruce Banner', age=40, team='Blue Team'),
        ]
        User.objects.bulk_create(users)

        # Save users individually to ensure they are persisted before being referenced
        for user in users:
            user.save()

        # Create teams with explicit IDs
        teams = [
            Team(id=1, name='Blue Team', members=[{'email': user.email, 'name': user.name} for user in users if user.team == 'Blue Team']),
            Team(id=2, name='Gold Team', members=[{'email': user.email, 'name': user.name} for user in users if user.team == 'Gold Team']),
        ]
        Team.objects.bulk_create(teams)

        # Ensure activities reference user IDs instead of user objects
        activities = [
            Activity(id=1, user_id=1, type='Cycling', duration=60, date=date(2025, 4, 1)),
            Activity(id=2, user_id=2, type='Crossfit', duration=120, date=date(2025, 4, 2)),
            Activity(id=3, user_id=3, type='Running', duration=90, date=date(2025, 4, 3)),
            Activity(id=4, user_id=4, type='Strength', duration=30, date=date(2025, 4, 4)),
            Activity(id=5, user_id=5, type='Swimming', duration=75, date=date(2025, 4, 5)),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=teams[0], points=300),
            Leaderboard(team=teams[1], points=250),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event', duration=60),
            Workout(name='Crossfit', description='High-intensity functional training', duration=120),
            Workout(name='Running Training', description='Training for a marathon', duration=90),
            Workout(name='Strength Training', description='Weightlifting and strength exercises', duration=30),
            Workout(name='Swimming Training', description='Training for a swimming competition', duration=75),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
