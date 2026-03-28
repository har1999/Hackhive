"""
Management command: python manage.py seed_demo
Creates realistic demo data for hackathon judging.
Workers with full history, contractors with posted jobs, ratings, endorsements.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, date
import random

User = get_user_model()


WORKER_DATA = [
    {'name': 'Raju Sharma', 'phone': '9876543201', 'skill': 'mason', 'location': 'Andheri West, Mumbai', 'lat': 19.1196, 'lng': 72.8468},
    {'name': 'Mohan Patel', 'phone': '9876543202', 'skill': 'electrician', 'location': 'Bhandup, Mumbai', 'lat': 19.1535, 'lng': 72.9407},
    {'name': 'Suresh Kumar', 'phone': '9876543203', 'skill': 'plumber', 'location': 'Kurla, Mumbai', 'lat': 19.0728, 'lng': 72.8826},
    {'name': 'Ramesh Yadav', 'phone': '9876543204', 'skill': 'painter', 'location': 'Dharavi, Mumbai', 'lat': 19.0416, 'lng': 72.8560},
    {'name': 'Arjun Singh', 'phone': '9876543205', 'skill': 'carpenter', 'location': 'Goregaon, Mumbai', 'lat': 19.1624, 'lng': 72.8499},
    {'name': 'Pappu Bind', 'phone': '9876543206', 'skill': 'labourer', 'location': 'Ghatkopar, Mumbai', 'lat': 19.0858, 'lng': 72.9081},
    {'name': 'Dinesh Thakur', 'phone': '9876543207', 'skill': 'welder', 'location': 'Vikhroli, Mumbai', 'lat': 19.1067, 'lng': 72.9264},
    {'name': 'Mahesh Gupta', 'phone': '9876543208', 'skill': 'tiler', 'location': 'Borivali, Mumbai', 'lat': 19.2307, 'lng': 72.8567},
]

CONTRACTOR_DATA = [
    {'name': 'Aarav Constructions', 'phone': '9876540001', 'company': 'Aarav Build Pvt Ltd', 'location': 'Andheri, Mumbai', 'lat': 19.1136, 'lng': 72.8697},
    {'name': 'Priya Builders', 'phone': '9876540002', 'company': 'Priya Infrastructure', 'location': 'BKC, Mumbai', 'lat': 19.0639, 'lng': 72.8653},
    {'name': 'Rahul Contractors', 'phone': '9876540003', 'company': 'Rahul & Sons Construction', 'location': 'Thane', 'lat': 19.2183, 'lng': 72.9781},
]

JOB_TITLES = {
    'mason': ['Brick wall construction', 'Foundation laying work', 'Block masonry for new floor', 'Boundary wall repair'],
    'electrician': ['Flat wiring work', 'Panel installation', 'AC point fitting', 'Office rewiring'],
    'plumber': ['Bathroom plumbing', 'Water tank installation', 'Pipe leakage repair', 'Drainage work'],
    'painter': ['Flat painting (2BHK)', 'Office exterior painting', 'Texture painting work', 'Wall putty & paint'],
    'carpenter': ['Door frame work', 'Kitchen cabinet fitting', 'Wooden flooring', 'Wardrobe installation'],
    'labourer': ['Construction site cleaning', 'Material loading/unloading', 'Demolition work', 'Digging & earthwork'],
    'welder': ['Grille fabrication', 'Gate welding', 'Stainless steel railing', 'Structural steel work'],
    'tiler': ['Floor tiling (1000 sqft)', 'Bathroom tile fixing', 'Kitchen tiles', 'Parking area tiles'],
}

ENDORSEMENT_TAGS = ['reads_plans', 'tiling_quality', 'punctual', 'plastering', 'clean_work', 'team_player', 'fast_worker']


class Command(BaseCommand):
    help = 'Seed demo data for KaamSetu hackathon demo'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding KaamSetu demo data...\n')

        from workers.models import WorkerProfile
        from contractors.models import ContractorProfile
        from jobs.models import Job, JobApplication, JobEngagement
        from ratings.models import Rating, SkillEndorsement

        # Admin
        if not User.objects.filter(phone='0000000000').exists():
            admin = User.objects.create_superuser(phone='0000000000', password='admin123', name='Admin')
            self.stdout.write('  ✅ Admin: phone=0000000000, pass=admin123')

        # Contractors
        contractors = []
        for cd in CONTRACTOR_DATA:
            user, created = User.objects.get_or_create(
                phone=cd['phone'],
                defaults={'name': cd['name'], 'role': 'contractor', 'is_verified': True}
            )
            cp, _ = ContractorProfile.objects.get_or_create(
                user=user,
                defaults={'company_name': cd['company'], 'location_name': cd['location'],
                          'latitude': cd['lat'], 'longitude': cd['lng']}
            )
            contractors.append(user)
            if created:
                self.stdout.write(f'  ✅ Contractor: {user.name} ({user.phone})')

        # Workers
        workers = []
        for wd in WORKER_DATA:
            user, created = User.objects.get_or_create(
                phone=wd['phone'],
                defaults={'name': wd['name'], 'role': 'worker', 'is_verified': True}
            )
            wp, _ = WorkerProfile.objects.get_or_create(
                user=user,
                defaults={'skill_category': wd['skill'], 'location_name': wd['location'],
                          'latitude': wd['lat'], 'longitude': wd['lng'], 'is_available': True}
            )
            workers.append((user, wp))
            if created:
                self.stdout.write(f'  ✅ Worker: {user.name} ({wd["skill"]})')

        # Jobs + Engagements + Ratings (historical)
        self.stdout.write('\n  📋 Creating job history...')
        engagement_count = 0

        for contractor in contractors:
            for worker_user, worker_profile in workers[:4]:
                skill = worker_profile.skill_category
                titles = JOB_TITLES.get(skill, ['Construction work'])

                for i in range(random.randint(3, 7)):
                    days_ago = random.randint(10, 365)
                    start = date.today() - timedelta(days=days_ago)
                    duration = random.choice([1, 2, 3, 5, 7])
                    rate = random.choice([400, 450, 500, 550, 600, 700])

                    job = Job.objects.create(
                        contractor=contractor,
                        title=random.choice(titles),
                        skill_category=skill,
                        location_name=contractor.contractor_profile.location_name,
                        latitude=contractor.contractor_profile.latitude or 19.076,
                        longitude=contractor.contractor_profile.longitude or 72.877,
                        daily_rate=rate,
                        workers_needed=1,
                        duration_days=duration,
                        start_date=start,
                        status='completed',
                        radius_km=10,
                    )
                    app = JobApplication.objects.create(job=job, worker=worker_user, status='hired', hired_at=timezone.now())
                    completed = timezone.now() - timedelta(days=days_ago - duration)
                    eng = JobEngagement.objects.create(
                        application=app, job=job, worker=worker_user, contractor=contractor,
                        status='completed', completed_at=completed,
                        contractor_marked_complete=True, worker_marked_complete=True
                    )

                    # Contractor rates worker
                    if not Rating.objects.filter(engagement=eng, direction='contractor_to_worker').exists():
                        score = random.choices([3, 4, 4, 5, 5], k=1)[0]
                        Rating.objects.create(
                            engagement=eng, rater=contractor, ratee=worker_user,
                            direction='contractor_to_worker', score=score,
                            note=random.choice(['Good work', 'Punctual and clean', 'Will hire again', 'Reliable mason', ''])
                        )

                    # Worker rates contractor
                    if not Rating.objects.filter(engagement=eng, direction='worker_to_contractor').exists():
                        score = random.choices([3, 4, 4, 5, 5], k=1)[0]
                        Rating.objects.create(
                            engagement=eng, rater=worker_user, ratee=contractor,
                            direction='worker_to_contractor', score=score,
                            note=random.choice(['Paid on time', 'Clear instructions', 'Good site', ''])
                        )

                    # Endorsements
                    tags = random.sample(ENDORSEMENT_TAGS, k=random.randint(1, 3))
                    for tag in tags:
                        SkillEndorsement.objects.get_or_create(
                            engagement=eng, contractor=contractor,
                            worker=worker_user, tag=tag
                        )

                    engagement_count += 1

        # Active open jobs
        self.stdout.write('\n  📌 Creating open jobs...')
        open_job_data = [
            ('Mason needed urgently', 'mason', True, 550, 19.1136, 72.8697),
            ('Electrician for 2BHK wiring', 'electrician', False, 600, 19.0639, 72.8653),
            ('Painter for office', 'painter', False, 450, 19.1196, 72.8468),
            ('Plumber — pipe leak fix', 'plumber', True, 500, 19.0728, 72.8826),
        ]
        for title, skill, urgent, rate, lat, lng in open_job_data:
            Job.objects.create(
                contractor=contractors[0],
                title=title, skill_category=skill,
                location_name='Mumbai',
                latitude=lat, longitude=lng,
                daily_rate=rate, workers_needed=2,
                duration_days=random.choice([1, 2, 3]),
                start_date=date.today(),
                is_urgent=urgent, status='open', radius_km=15,
            )

        self.stdout.write(f'\n✅ Seeding complete!')
        self.stdout.write(f'   Workers: {len(workers)}')
        self.stdout.write(f'   Contractors: {len(contractors)}')
        self.stdout.write(f'   Engagements: {engagement_count}')
        self.stdout.write(f'\n🔑 Login: any worker phone (e.g. 9876543201) — OTP shown in console')
        self.stdout.write(f'   Contractor: 9876540001 | Admin: 0000000000 / admin123')
