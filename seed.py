"""Starter content for the RemoteTravels site.

The data mirrors the original static website so the Flask application boots
with the same content. Every record can be edited later from the admin area
(``/admin``) or through the shell (``flask shell``).
"""

from .extensions import db
from .models import (
    Destination,
    Experience,
    Feature,
    JobPosting,
    LegalPage,
    Package,
    Service,
    SiteSetting,
    Testimonial,
    Touchpoint,
    Wildlife,
)

LOGO_URL = 'https://i.pinimg.com/736x/d2/3d/d8/d23dd8ad0a03ce25635349483c6e7130.jpg'

SETTINGS = {
    'company_name': 'RemoteTravels',
    'tagline': 'Discover Extraordinary',
    'phone': '+254 711 697 080',
    'email': 'info@remotetravels.com',
    'address': 'Narok, Olmaa House room 10 along Narok-Mai-mahiu road, Kenya',
    'hours': 'Mon-Fri: 8AM - 6PM, Sat: 9AM - 4PM',
    'whatsapp': '254711697080',
    'admin_email': 'info@remotetravels.co.ke',
    'hero_title': 'Discover Extraordinary Journeys',
    'hero_subtitle': "Experience breathtaking adventures, discover hidden gems, and create unforgettable memories with our expertly crafted tours.",
    'logo_url': LOGO_URL,
    'facebook': 'https://www.facebook.com/',
    'twitter': 'https://twitter.com/',
    'instagram': 'https://www.instagram.com/',
    'youtube': 'https://www.youtube.com/',
    'pinterest': '#',
}

DESTINATIONS = [
    {
        'name': 'Maasai Mara Safari',
        'tag': 'Safari',
        'location': 'Kenya',
        'price': '$1,299',
        'price_value': 1299,
        'duration_days': 7,
        'image_url': 'https://images.unsplash.com/photo-1523805009345-7448845a9e53?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
        'description': "Witness the Great Migration and Africa's Big Five in their natural habitat. Experience thrilling game drives and authentic Maasai cultural encounters. Our expert guides will take you through the vast savannahs where you'll encounter lions, elephants, and the majestic wildebeest migration.",
        'highlights': [
            'Great Migration river crossings',
            'Big Five game drives',
            'Maasai cultural village visit',
            'Hot air balloon safari',
            'Luxury tented camp accommodation',
        ],
        'is_featured': True,
        'sort_order': 1,
    },
    {
        'name': 'Burj Khalifa Experience',
        'tag': 'Luxury',
        'location': 'Dubai, UAE',
        'price': '$1,899',
        'price_value': 1899,
        'duration_days': 5,
        'image_url': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
        'description': "Visit the world's tallest building and enjoy panoramic views of Dubai. Experience luxury shopping, desert safaris, and stunning modern architecture. Stay in 5-star accommodations and enjoy exclusive access to the observation deck on the 148th floor.",
        'highlights': [
            'Burj Khalifa At The Top',
            'Private desert safari',
            'Yacht cruise along the Marina',
            'Dubai Mall and souk shopping',
            '5-star city accommodation',
        ],
        'is_featured': True,
        'sort_order': 2,
    },
    {
        'name': 'Kilimanjaro Summit',
        'tag': 'Adventure',
        'location': 'Tanzania',
        'price': '$2,499',
        'price_value': 2499,
        'duration_days': 9,
        'image_url': 'https://i.pinimg.com/736x/5e/dc/21/5edc212561aef0a633c45f0d0863cedb.jpg',
        'description': "Conquer Africa's highest peak with expert guides. Experience diverse ecosystems from rainforest to arctic summit on this life-changing adventure. Our carefully planned 9-day itinerary ensures proper acclimatization and maximizes your chances of reaching the summit.",
        'highlights': [
            'Seven day climb to Uhuru Peak',
            'Certified mountain guides',
            'Full camp equipment provided',
            'Pre-climb training session',
            'Zanzibar beach extension',
        ],
        'is_featured': True,
        'sort_order': 3,
    },
    {
        'name': 'San Miguel, Italy',
        'tag': 'Luxury',
        'location': 'Italy',
        'price': '$1,899',
        'price_value': 1899,
        'duration_days': 5,
        'image_url': 'https://i.pinimg.com/1200x/5e/bf/5c/5ebf5c681fce5df728ca902c8eb9ae9f.jpg',
        'description': "Welcome to San Miguel, a picturesque and enchanting town nestled in the heart of Mexico. At Remote Tours, we invite you to discover the beauty, culture, and charm of this hidden gem. Enjoy gourmet dining, vineyard tours, and luxurious accommodations in historic villas.",
        'highlights': [
            'Historic villa accommodation',
            'Vineyard and winery tours',
            'Gourmet dining experiences',
            'Guided heritage walking tour',
            'Private airport transfers',
        ],
        'is_featured': True,
        'sort_order': 4,
    },
    {
        'name': 'Maldives Getaway',
        'tag': 'Luxury',
        'location': 'Maldives',
        'price': '$2,199',
        'price_value': 2199,
        'duration_days': 6,
        'image_url': 'https://i.pinimg.com/736x/fb/58/fa/fb58fa3c469e496e520c25e412c86b97.jpg',
        'description': "Located in the pristine Raa Atoll, the InterContinental Maldives Maamunagau Resort is a fine mix of luxury and natural beauty. Make the most of the gorgeous lagoon and its marine life with private overwater villas, spa treatments, and world-class diving opportunities.",
        'highlights': [
            'Private overwater villa',
            'House reef diving',
            'Sunset dolphin cruise',
            'Spa and wellness treatments',
            'All-inclusive dining',
        ],
        'is_featured': True,
        'sort_order': 5,
    },
    {
        'name': 'Kailasa Temple Experience',
        'tag': 'Adventure',
        'location': 'India',
        'price': '$1,599',
        'price_value': 1599,
        'duration_days': 8,
        'image_url': 'https://i.pinimg.com/1200x/09/94/0d/09940d0dbdb9d3484a7e6c83fbc4a34d.jpg',
        'description': "Step into the awe-inspiring Kailasa Temple at Ellora—India's largest monolithic monument. Carved in the 8th century directly from living rock, its soaring pillars, intricate sculptures, and cascading relief panels celebrate Hindu mythology in breathtaking detail. Explore surrounding caves and ancient ruins.",
        'highlights': [
            'Guided Kailasa Temple walk-through',
            'Ellora caves exploration',
            'Ajanta and Ellora heritage guide',
            'Local vegetarian thali lunch',
            'Heritage hotel stay',
        ],
        'is_featured': True,
        'sort_order': 6,
    },
]

PACKAGES = [
    {
        'name': 'African Safari',
        'tagline': 'Ten days across Kenya and Tanzania',
        'price': '$2,499',
        'price_value': 2499,
        'days': 10,
        'nights': 9,
        'highlight': 'Most Popular',
        'tags': ['Wildlife', 'Adventure', 'Luxury'],
        'features': [
            'Luxury lodge accommodations',
            'Daily game drives',
            'Maasai cultural experience',
            'Hot air balloon safari',
            'All meals included',
            'Professional photographer guide',
        ],
        'comparison': {
            'Accommodation Type': 'Luxury Lodges',
            'Meals Included': '<i class="fas fa-check"></i> All Meals',
            'Physical Difficulty': 'Easy',
            'Group Size': 'Max 12 people',
            'Guide Included': '<i class="fas fa-check"></i> Wildlife Expert',
            'Transportation': 'Private Safari Vehicle',
        },
        'is_featured': True,
        'sort_order': 1,
    },
    {
        'name': 'Desert Adventure',
        'tagline': 'Dubai desert experiences and city highlights',
        'price': '$3,199',
        'price_value': 3199,
        'days': 7,
        'nights': 6,
        'highlight': 'Best Value',
        'tags': ['Desert', 'Luxury', 'City Tour'],
        'features': [
            'Burj Khalifa At The Top experience',
            'Luxury desert camp stay',
            'Dune bashing & camel riding',
            'Private yacht tour',
            'Gourmet dining experiences',
            'Helicopter city tour',
        ],
        'comparison': {
            'Accommodation Type': '5-Star Hotels & Desert Camp',
            'Meals Included': '<i class="fas fa-check"></i> Breakfast & Dinner',
            'Physical Difficulty': 'Moderate',
            'Group Size': 'Max 10 people',
            'Guide Included': '<i class="fas fa-check"></i> Local Culture Expert',
            'Transportation': 'Luxury SUV & Private Yacht',
        },
        'is_featured': True,
        'sort_order': 2,
    },
    {
        'name': 'Mountain Expedition',
        'tagline': 'Summit Kilimanjaro with expert guides',
        'price': '$3,899',
        'price_value': 3899,
        'days': 14,
        'nights': 13,
        'highlight': None,
        'tags': ['Adventure', 'Hiking', 'Challenge'],
        'features': [
            'Kilimanjaro summit climb',
            'Professional mountain guides',
            'All camping equipment provided',
            'Pre-climb training & preparation',
            'Post-climb Zanzibar beach extension',
            'Medical support & insurance',
        ],
        'comparison': {
            'Accommodation Type': 'Mountain Camps',
            'Meals Included': '<i class="fas fa-check"></i> All Meals',
            'Physical Difficulty': 'Challenging',
            'Group Size': 'Max 8 people',
            'Guide Included': '<i class="fas fa-check"></i> Mountain Guide',
            'Transportation': '4x4 Vehicles',
        },
        'is_featured': True,
        'sort_order': 3,
    },
]

EXPERIENCES = [
    {
        'title': 'Safari Adventure in the Maasai Mara',
        'duration': '6 days',
        'highlights': 'Night drives, riverbank sightings, expert-led tracking. Maasai Mara National Reserve, Big Five safari, cultural interactions with the Maasai, hot air balloon safari, game drives, and luxury tented camp accommodations.',
        'price': 'USD 1,499',
        'image_url': 'https://i.pinimg.com/1200x/86/86/9c/86869c393b7645fb194d62f96751db6a.jpg',
        'sort_order': 1,
    },
    {
        'title': 'Cultural Discovery in Nairobi and Beyond',
        'duration': '5 days',
        'highlights': 'Nairobi city tour, Karen Blixen Museum, Giraffe Centre, David Sheldrick Wildlife Trust, Maasai Market, and a visit to a Maasai village.',
        'price': 'USD 1,299',
        'image_url': 'https://i.pinimg.com/736x/77/00/f6/7700f64cc9e83ca46e2e98d6a9040053.jpg',
        'sort_order': 2,
    },
    {
        'title': 'Beach Retreat in Mombasa',
        'duration': '4 days',
        'highlights': "Relaxation on Diani Beach, water sports, snorkeling at Kisite-Mpunguti Marine National Park, and exploring Mombasa's historic Old Town.",
        'price': 'USD 999',
        'image_url': 'https://i.pinimg.com/1200x/1d/2f/2b/1d2f2b667be468b9594063e5c235e790.jpg',
        'sort_order': 3,
    },
]

WILDLIFE = [
    {
        'name': 'The Majestic Lion',
        'tag': 'King of the Jungle',
        'image_url': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
        'description': 'Symbolizing courage and leadership, the lion reigns as the king of the savannah. Witness these magnificent predators in their natural habitat during our Maasai Mara safari adventures.',
    },
    {
        'name': 'The Gentle Elephant',
        'tag': 'Gentle Giants',
        'image_url': 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
        'description': 'Representing wisdom and strength, elephants form deep family bonds. Experience close encounters with these gentle giants in Amboseli National Park with Kilimanjaro as your backdrop.',
    },
    {
        'name': 'The Elusive Leopard',
        'tag': 'Master of Stealth',
        'image_url': 'https://i.pinimg.com/736x/03/43/3a/03433a7dbe6d5b9ba45068910c091ffb.jpg',
        'description': "Embodying grace and mystery, leopards are nature's perfect predators. Join our specialized safari tours for a chance to spot these elusive cats in Zambia's South Luangwa National Park.",
    },
    {
        'name': 'The Graceful Giraffe',
        'tag': 'Towers of the Savannah',
        'image_url': 'https://i.pinimg.com/736x/c8/e7/5a/c8e75a897e5b0c209311d6a90ccb8646.jpg',
        'description': "With their elegant stature, giraffes symbolize perspective and intuition. Observe these gentle creatures in the Serengeti during the Great Migration for an unforgettable experience.",
    },
    {
        'name': 'The Mighty Rhino',
        'tag': 'Ancient Guardians',
        'image_url': 'https://i.pinimg.com/736x/36/5f/2f/365f2fb2c3a0b28173d8ae75a0a3c521.jpg',
        'description': "Representing resilience and protection, rhinos are living relics of prehistoric times. Support conservation efforts by joining our rhino-tracking tours in Kenya's protected reserves.",
    },
    {
        'name': 'The Speedy Cheetah',
        'tag': 'Speed of Nature',
        'image_url': 'https://i.pinimg.com/1200x/69/23/a0/6923a01882a68f8e7c86c2a4066ba27d.jpg',
        'description': "Epitomizing speed and focus, cheetahs are nature's fastest land animals. Witness their incredible hunting prowess during our early morning game drives in the Maasai Mara.",
    },
]

SERVICES = [
    {
        'title': 'Group Getaways',
        'icon': 'fa-users',
        'description': 'At RemoteTravels, we believe that the joy of travel is amplified when shared with friends, family, or like-minded individuals.',
    },
    {
        'title': 'Family Vacations',
        'icon': 'fa-user-friends',
        'description': 'At RemoteTravels, we understand that family vacations are a time to connect, explore, and make memories that will last a lifetime.',
    },
    {
        'title': 'Honeymoons',
        'icon': 'fa-gem',
        'description': 'Let us help you create a romantic and unforgettable honeymoon experience that perfectly matches your dreams.',
    },
    {
        'title': 'Destination Weddings',
        'icon': 'fa-snowflake',
        'description': "A destination wedding is more than just a ceremony; it's an unforgettable experience.",
    },
]

FEATURES = [
    {
        'title': '5-Star Reviews',
        'icon': 'fa-award',
        'description': 'Over 1,200 glowing testimonials on TripAdvisor & Google—our happiest travelers speak for us.',
    },
    {
        'title': 'Local Expert Guides',
        'icon': 'fa-hands-helping',
        'description': 'Every tour is led by certified, bilingual guides native to your destination—authentic stories guaranteed.',
    },
    {
        'title': 'Traveler Rewards',
        'icon': 'fa-gift',
        'description': 'Join our Adventure Club to earn points on every booking—redeem them for free excursions, upgrades, and more.',
    },
    {
        'title': 'Sustainable Travel',
        'icon': 'fa-leaf',
        'description': 'We partner with local communities and eco-lodges to ensure your adventure gives back to the planet.',
    },
    {
        'title': '24/7 Support',
        'icon': 'fa-phone-volume',
        'description': 'Our global support team is available around the clock—help is always just a call or chat away.',
    },
    {
        'title': 'Risk-Free Booking',
        'icon': 'fa-shield-alt',
        'description': 'Flexible cancellations, transparent pricing, and full travel insurance options—peace of mind included.',
    },
]

TOUCHPOINTS = [
    {
        'title': 'Narok Town Centre (Market Roundabout)',
        'image_url': 'https://i.pinimg.com/736x/6f/3b/9a/6f3b9a9ac3a039004930715b2b710223.jpg',
        'bullets': [
            'Welcome Desk: Our friendly RemoteTravels greeters meet you curbside, provide bottled water, SIM cards, and local maps.',
            'Local Insights: Discover fresh produce, handcrafted beadwork, and authentic street-food stalls before heading out on safari.',
        ],
    },
    {
        'title': 'Safari Lodge and Hotel Lobbies',
        'image_url': 'https://i.pinimg.com/1200x/02/01/02/02010213ac6383a645e40cdabf02c876.jpg',
        'bullets': [
            'Personalized Check-In: We fast-track your arrival with pre-booked rooms, complimentary tea, and an orientation to lodge amenities.',
            '24/7 Lounge Concierge: From dinner reservations to spa bookings, our on-site reps handle all your needs so you can relax and recharge.',
        ],
    },
    {
        'title': 'Safari Vehicle Parks',
        'image_url': 'https://i.pinimg.com/736x/50/8a/65/508a65b7d13d0f7af3282ece5f8380a6.jpg',
        'bullets': [
            'Branded Waiting Areas: Shaded benches, charging stations, and light refreshments keep you comfortable while your guide prepares your vehicle.',
            'Pre-Drive Briefing: Every excursion begins with a safety talk—covering radio protocols, wildlife etiquette, and our emergency pickup plan.',
        ],
    },
]

TESTIMONIALS = [
    {
        'author': 'Sarah Johnson',
        'trip': 'African Safari Adventure',
        'quote': "The Maasai Mara safari exceeded all our expectations. Our guide's knowledge of wildlife was incredible - we saw the Big Five in just three days! The luxury lodges were beyond comfortable after exciting days of game drives.",
        'image_url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80',
    },
    {
        'author': 'Michael Chen',
        'trip': 'Desert Adventure',
        'quote': 'Our Dubai experience was pure luxury. From the Burj Khalifa views to our private yacht dinner, everything was perfectly arranged. The desert safari was the highlight - dune bashing at sunset followed by a gourmet feast under the stars.',
        'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80',
    },
    {
        'author': 'Emma Rodriguez',
        'trip': 'Kilimanjaro Expedition',
        'quote': "Reaching the summit of Kilimanjaro was the most challenging and rewarding experience of my life. The RemoteTravels team provided exceptional support that made all the difference. Their attention to safety and comfort was outstanding.",
        'image_url': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80',
    },
]

JOBS = [
    {
        'title': 'Driver',
        'summary': 'We are seeking a reliable and responsible Driver to join our team. The ideal candidate will ensure safe transportation of goods and/or passengers to their destinations, while adhering to all traffic laws and company policies. As a Driver, you will play a crucial role in representing our company and providing a positive customer experience.',
        'responsibilities': [
            'Safely operate and maintain company vehicles.',
            'Transport goods and/or passengers to designated locations.',
            'Follow all traffic laws and regulations.',
            'Keep the vehicle clean and in good working condition.',
            'Perform routine vehicle inspections and maintenance.',
            'Ensure the safety of passengers and cargo.',
            'Provide excellent customer service and assistance.',
            'Maintain accurate records of trips and expenses.',
            'Report any incidents or accidents promptly.',
            'Adhere to company policies and procedures.',
        ],
        'qualifications': [
            "Valid driver's license and a clean driving record.",
            'Previous experience as a driver is preferred.',
            'Knowledge of local routes and traffic patterns.',
            'Strong communication and interpersonal skills.',
            'Ability to work independently and responsibly.',
            'Excellent problem-solving skills.',
            'Physical ability to load and unload goods (if applicable).',
        ],
    },
    {
        'title': 'Tour Guide',
        'summary': "We are looking for enthusiastic and knowledgeable Tour Guides to lead our guests on informative and engaging tours. As a Tour Guide, you will provide valuable information, share interesting stories, and ensure an enjoyable experience for our visitors. If you have a passion for the area's history, culture, and attractions, we want you on our team.",
        'responsibilities': [
            'Conduct guided tours for groups of visitors.',
            'Provide informative and engaging commentary.',
            'Ensure the safety and comfort of tour participants.',
            'Answer questions and provide assistance to guests.',
            "Maintain a high level of knowledge about the tour's subject matter.",
            'Promote a positive and memorable experience for visitors.',
            'Handle reservations and ticketing (if applicable).',
            'Follow tour schedules and itineraries.',
        ],
        'qualifications': [
            'Passion for the subject matter (e.g., local history, art, nature).',
            'Excellent communication and public speaking skills.',
            'Friendly and approachable demeanor.',
            'Ability to adapt to different audiences.',
            'Strong organizational and time-management skills.',
            'Customer service-oriented attitude.',
            'Multilingual skills (if applicable) may be a plus.',
        ],
    },
    {
        'title': 'Account Officer',
        'summary': 'We are seeking a detail-oriented and results-driven Account Officer to manage financial transactions, reconcile accounts, and assist in financial reporting. The ideal candidate will have a strong understanding of financial principles and be able to work collaboratively with our finance team to ensure accurate and timely financial operations.',
        'responsibilities': [
            'Maintain and reconcile financial records and accounts.',
            'Process and verify invoices and receipts.',
            'Assist in preparing financial statements and reports.',
            'Monitor and track financial transactions.',
            'Collaborate with other departments on financial matters.',
            'Ensure compliance with financial regulations and policies.',
            'Prepare and process payroll (if applicable).',
            'Assist with budgeting and forecasting.',
        ],
        'qualifications': [
            "Bachelor's degree in finance, accounting, or a related field.",
            'Previous experience in accounting or finance roles.',
            'Knowledge of financial software and tools.',
            'Strong analytical and problem-solving skills.',
            'Attention to detail and accuracy.',
            'Excellent communication and interpersonal skills.',
            'Ability to work independently and as part of a team.',
        ],
    },
    {
        'title': 'Secretary',
        'summary': 'We are looking for an organized and efficient Secretary to provide administrative support to our team. The Secretary will be responsible for managing office tasks, scheduling appointments, handling communications, and maintaining office records. The ideal candidate is highly organized, detail-oriented, and proficient in office software and communication.',
        'responsibilities': [
            'Answer and direct phone calls and emails.',
            'Schedule appointments and manage calendars.',
            'Prepare and organize documents and reports.',
            'Assist in the coordination of meetings and events.',
            'Maintain office filing systems and records.',
            'Handle incoming and outgoing mail and packages.',
            'Order and maintain office supplies and equipment.',
            'Greet and assist visitors in a friendly and professional manner.',
            'Assist with travel arrangements (if applicable).',
            'Perform general clerical tasks as needed.',
        ],
        'qualifications': [
            'High school diploma or equivalent; additional education or certification is a plus.',
            'Proven experience as a secretary or administrative assistant.',
            'Proficiency in office software (e.g., Microsoft Office Suite).',
            'Strong organizational and time-management skills.',
            'Excellent written and verbal communication skills.',
            'Attention to detail and accuracy.',
            'Ability to handle sensitive and confidential information.',
            'Friendly and professional demeanor.',
        ],
    },
]

PRIVACY_CONTENT = """
<h2 data-number="0.">Privacy Policy</h2>
<p>Thank you for choosing Remote Travels. This Privacy Policy describes how we collect, use, and disclose personal information when you use our website and services.</p>

<h2 data-number="1.">Information We Collect</h2>
<h3 data-number="1.1.">Personal Information:</h3>
<p>We may collect personal information such as names, addresses, phone numbers, and email addresses when you make a reservation or use our services.</p>
<h3 data-number="1.2.">Payment Information:</h3>
<p>We collect payment information when you make a booking, including credit card details. This information is securely processed and not stored on our servers.</p>
<h3 data-number="1.3.">Travel Details:</h3>
<p>We may collect information about your travel plans, preferences, and special requests to provide you with a customized experience.</p>
<h3 data-number="1.4.">Log Data:</h3>
<p>Our servers automatically record information when you visit our website, including your IP address, browser type, and the pages you access.</p>

<h2 data-number="2.">How We Use Your Information</h2>
<h3 data-number="2.1.">Service Provision:</h3>
<p>We use your information to fulfill bookings, provide services, and communicate with you about your travel plans.</p>
<h3 data-number="2.2.">Marketing:</h3>
<p>With your consent, we may send you promotional materials and updates about our services. You can opt-out at any time.</p>
<h3 data-number="2.3.">Analytics:</h3>
<p>We use data for analytics purposes to improve our website, services, and customer experience.</p>
<h3 data-number="2.4.">Legal Compliance:</h3>
<p>We may use your information to comply with legal obligations or resolve disputes.</p>

<h2 data-number="3.">How We Share Your Information</h2>
<h3 data-number="3.1.">Service Providers:</h3>
<p>We may share your information with third-party service providers who assist us in delivering our services.</p>
<h3 data-number="3.2.">Legal Requirements:</h3>
<p>We may disclose your information if required by law or to protect our rights and safety.</p>
<h3 data-number="3.3.">Business Transfers:</h3>
<p>In the event of a merger, acquisition, or sale of all or part of our assets, your information may be transferred.</p>

<h2 data-number="4.">Your Choices and Rights</h2>
<h3 data-number="4.1.">Access and Correction:</h3>
<p>You have the right to access and correct your personal information. Contact us at info@remotetravels.co.ke for assistance.</p>
<h3 data-number="4.2.">Opt-Out:</h3>
<p>You can opt-out of receiving marketing communications by following the instructions in the communication or contacting us directly.</p>

<h2 data-number="5.">Security</h2>
<p>We take reasonable measures to protect your information from unauthorized access, disclosure, alteration, or destruction.</p>

<h2 data-number="6.">Children's Privacy</h2>
<p>Our services are not directed to individuals under the age of 18. We do not knowingly collect personal information from children. If you are a parent or guardian and believe your child has provided us with personal information, please contact us.</p>

<h2 data-number="7.">Changes to this Privacy Policy</h2>
<p>We may update this Privacy Policy from time to time. We will notify you of any significant changes by posting the updated policy on our website.</p>

<h2 data-number="8.">Contact Us</h2>
<p>For any inquiries or concerns regarding these terms and conditions, please contact us at:</p>
<p>
    P. O. Box 2874-30100, Eldoret<br>
    +254 711 697 080<br>
    <a href="mailto:info@remotetravels.co.ke">info@remotetravels.co.ke</a> or <a href="mailto:remotetravels@gmail.com">remotetravels@gmail.com</a>
</p>
"""

TERMS_CONTENT = """
<h2>Acceptance of Terms</h2>
<p>By accessing and using the services provided by Remote Travels, you agree to comply with and be bound by the terms and conditions outlined herein. If you do not agree with any part of these terms, please refrain from using our services.</p>

<h2>Booking and Payments</h2>
<h3 data-number="2.1">Reservations:</h3>
<p>All bookings are subject to availability and confirmation. Remote Travels reserves the right to refuse any booking.</p>
<h3 data-number="2.2">Payment:</h3>
<p>Payment for services must be made in full at the time of booking unless otherwise agreed upon. Prices are in USD ($), and any additional charges will be clearly stated. If payment is made in the local currency KES, the conversion will be done using the current dollar rate.</p>

<h2>Cancellation and Refunds</h2>
<h3 data-number="3.1">Cancellation by Customer:</h3>
<p>Cancellation policies vary by service. Please refer to specific tour or travel details for cancellation terms. Refunds may be subject to cancellation fees.</p>
<h3 data-number="3.2">Cancellation by RemoteTravels:</h3>
<p>In the event of unforeseen circumstances or insufficient bookings, Remote Travels reserves the right to cancel or modify a tour. In such cases, customers will be offered an alternative or a full refund.</p>

<h2>Travel Documents and Insurance</h2>
<h3 data-number="4.1">Documentation:</h3>
<p>It is the customer's responsibility to ensure all travel documents are in order, including passports, visas, and any other required documentation.</p>
<h3 data-number="4.2">Insurance:</h3>
<p>Remote Travels recommends that customers obtain comprehensive travel insurance covering cancellations, medical emergencies, and other unforeseen events.</p>

<h2>Changes to Itineraries</h2>
<p>Remote Travels reserves the right to alter itineraries due to unforeseen circumstances or events beyond our control. Every effort will be made to provide a comparable alternative.</p>

<h2>Code of Conduct</h2>
<p>Customers are expected to adhere to a code of conduct during tours. Any behavior deemed disruptive or disrespectful may result in removal from the tour without refund.</p>

<h2>Liability</h2>
<p>Remote Travels is not liable for personal injury, property damage, or other losses arising from participation in our tours, except where negligence is proven.</p>

<h2>Privacy Policy</h2>
<p>Our privacy policy outlines how Remote Travels collects, uses, and protects customer information. By using our services, you agree to our privacy policy.</p>

<h2>Governing Law</h2>
<p>These terms and conditions are governed by the laws of Kenya. Any disputes will be resolved in the courts of Kenya.</p>

<h2>Contact Information</h2>
<p>For any inquiries or concerns regarding these terms and conditions, please contact us at:</p>
<p>
    P. O. Box 2874-30100, Eldoret<br>
    +254 711 697 080<br>
    <a href="mailto:info@remotetravels.co.ke">info@remotetravels.co.ke</a> or <a href="mailto:remotetravels@gmail.com">remotetravels@gmail.com</a>
</p>
"""

CANCELLATION_CONTENT = """
<h1>Refund &amp; Cancellation Policy</h1>
<p class="intro">Thank you for choosing RemoteTravels. We value your business and want to ensure your experience with our tours and travel services is enjoyable. Please read our Refund and Cancellation Policy carefully.</p>

<h2 data-number="1.">Booking Cancellations</h2>
<h3 data-number="1.1.">Customer Cancellations</h3>
<p><strong>1.1.1 Cancellation Period:</strong> Customers may cancel bookings within a specified period. The cancellation period and associated fees vary by tour/package. Please refer to your booking confirmation for details.</p>
<p><strong>1.1.2 Cancellation Fees:</strong> Cancellation fees may apply. The amount depends on the timing of the cancellation relative to the start date of the tour. Details of these fees are outlined in your booking confirmation.</p>
<p><strong>1.1.3 Refund Process:</strong> To cancel a booking and request a refund, please contact us at <a href="mailto:info@remotetravels.co.ke">info@remotetravels.co.ke</a>. Refunds, if applicable, will be processed in accordance with the terms outlined in your booking confirmation.</p>

<h3 data-number="1.2.">RemoteTravels Cancellations</h3>
<p><strong>1.2.1 Unforeseen Circumstances:</strong> In rare instances, RemoteTravels may need to cancel a tour due to unforeseen circumstances such as extreme weather, natural disasters, or other events beyond our control.</p>
<p><strong>1.2.2 Alternative Arrangements:</strong> In the event of a cancellation by RemoteTravels, we will make every effort to offer customers an alternative tour or provide a full refund.</p>

<h2 data-number="2.">Refunds</h2>
<h3 data-number="2.1.">Eligibility</h3>
<p><strong>2.1.1 Valid Reasons:</strong> Refunds are typically provided for cancellations due to valid reasons such as medical emergencies or other unforeseen circumstances. Supporting documentation may be required.</p>
<p><strong>2.1.2 Non-Refundable Services:</strong> Some services, such as non-refundable hotel reservations or tickets to specific events, may not be eligible for a refund. Details will be provided at the time of booking.</p>

<h3 data-number="2.2.">Refund Process</h3>
<p><strong>2.2.1 Refund Requests:</strong> To request a refund, please contact us at <a href="mailto:info@remotetravels.co.ke">info@remotetravels.co.ke</a> with your booking details and the reason for the refund.</p>
<p><strong>2.2.2 Processing Time:</strong> Refunds, if approved, will be processed within 15 days of receiving the refund request. The processing time may vary depending on the payment method used.</p>

<h2 data-number="3.">Modifications to Bookings</h2>
<h3 data-number="3.1.">Changes by Customers</h3>
<p><strong>3.1.1 Modification Requests:</strong> If you need to make changes to your booking, please contact us as soon as possible. We will do our best to accommodate changes, but they may be subject to availability and additional fees.</p>

<h3 data-number="3.2.">Changes by RemoteTravels</h3>
<p><strong>3.2.1 Itinerary Modifications:</strong> RemoteTravels reserves the right to make changes to tour itineraries due to unforeseen circumstances. We will inform customers of any significant changes and offer suitable alternatives.</p>

<h2 data-number="4.">Contact Us</h2>
<p>If you have any questions or concerns about our Refund and Cancellation Policy, please contact us at <a href="mailto:info@remotetravels.co.ke">info@remotetravels.co.ke</a>.</p>

<h2 data-number="5.">Contact Information</h2>
<p>For any inquiries or concerns regarding these terms and conditions, please contact us at:</p>
<p>
    P. O. Box 2874-30100, Eldoret<br>
    +254 711 697 080<br>
    <a href="mailto:info@remotetravels.co.ke">info@remotetravels.co.ke</a>
</p>
"""

LEGAL_PAGES = [
    {
        'slug': 'privacy',
        'title': 'Privacy Policy',
        'hero_title': 'View our Policies',
        'hero_subtitle': 'Review our policies for a smooth and informed travel experience',
        'content': PRIVACY_CONTENT,
    },
    {
        'slug': 'terms',
        'title': 'Terms and Conditions',
        'hero_title': 'Terms and conditions',
        'hero_subtitle': 'Understand the terms that guide your travel experience with us',
        'content': TERMS_CONTENT,
    },
    {
        'slug': 'cancellation',
        'title': 'Cancellation Policy',
        'hero_title': 'Cancellations policy',
        'hero_subtitle': 'Plans change—our flexible cancellation terms let you adjust or cancel your booking hassle-free.',
        'content': CANCELLATION_CONTENT,
    },
]


def seed_all():
    """Insert the starter content. Existing rows are left untouched."""
    _seed_settings()
    _seed_destinations()
    _seed_packages()
    _seed_experiences()
    _seed_wildlife()
    _seed_services()
    _seed_features()
    _seed_touchpoints()
    _seed_testimonials()
    _seed_jobs()
    _seed_legal_pages()


def _seed_settings():
    for key, value in SETTINGS.items():
        if SiteSetting.query.filter_by(key=key).first() is None:
            db.session.add(SiteSetting(key=key, value=value))


def _seed_destinations():
    if Destination.query.count():
        return
    for data in DESTINATIONS:
        db.session.add(Destination(**data))


def _seed_packages():
    if Package.query.count():
        return
    for data in PACKAGES:
        db.session.add(Package(**data))


def _seed_experiences():
    if Experience.query.count():
        return
    for data in EXPERIENCES:
        db.session.add(Experience(**data))


def _seed_wildlife():
    if Wildlife.query.count():
        return
    for data in WILDLIFE:
        db.session.add(Wildlife(**data))


def _seed_services():
    if Service.query.count():
        return
    for data in SERVICES:
        db.session.add(Service(**data))


def _seed_features():
    if Feature.query.count():
        return
    for data in FEATURES:
        db.session.add(Feature(**data))


def _seed_touchpoints():
    if Touchpoint.query.count():
        return
    for data in TOUCHPOINTS:
        db.session.add(Touchpoint(**data))


def _seed_testimonials():
    if Testimonial.query.count():
        return
    for data in TESTIMONIALS:
        db.session.add(Testimonial(**data))


def _seed_jobs():
    if JobPosting.query.count():
        return
    for data in JOBS:
        db.session.add(JobPosting(**data))


def _seed_legal_pages():
    for data in LEGAL_PAGES:
        if LegalPage.query.filter_by(slug=data['slug']).first() is None:
            db.session.add(LegalPage(**data))
