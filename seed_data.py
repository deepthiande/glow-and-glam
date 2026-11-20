import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glowglam_project.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Category, Brand, Product, ProductImage, ProductShade, Review
from cart.models import Coupon
from orders.models import Order, OrderItem
from accounts.models import UserProfile

def seed():
    print("Clearing existing sample data...")
    Review.objects.all().delete()
    ProductShade.objects.all().delete()
    ProductImage.objects.all().delete()
    Product.objects.all().delete()
    Brand.objects.all().delete()
    Category.objects.all().delete()
    Coupon.objects.all().delete()

    # 1. Create Brands
    print("Creating luxury brands...")
    brands_data = [
        {"name": "Glow & Glam Haute", "slug": "glow-glam-haute", "description": "Our signature line of high-performance luxury cosmetics designed to illuminate your natural grace."},
        {"name": "Velvet Rose Paris", "slug": "velvet-rose-paris", "description": "Classic French elegance formulated with precious rose extracts and nourishing botanicals."},
        {"name": "Celestial Glow", "slug": "celestial-glow", "description": "Ultra-radiant highlighters and bronzers crafted for effortless multidimensional glow."},
        {"name": "Lumière Botanicals", "slug": "lumiere-botanicals", "description": "100% vegan, clean skincare and base makeup infused with certified organic extracts."},
        {"name": "Petal Soft London", "slug": "petal-soft-london", "description": "Featherlight complexion enhancers and velvet matte lip formulations with weightless textures."},
        {"name": "Nude Alchemy", "slug": "nude-alchemy", "description": "Inclusive, undertone-perfect complexion products crafted for every skin shade and texture."},
    ]
    brand_objs = {}
    for b in brands_data:
        brand_objs[b['slug']], _ = Brand.objects.get_or_create(
            slug=b['slug'],
            defaults={'name': b['name'], 'description': b['description']}
        )

    # 2. Create the 10 Required Categories
    print("Creating the 10 product categories...")
    categories_data = [
        {
            "name": "Lipsticks",
            "slug": "lipsticks",
            "icon": "fa-kiss-wink-heart",
            "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?q=80&w=800&auto=format&fit=crop",
            "description": "Velvety matte, glossy satin, and hydrating sheer formulas in universally flattering shades.",
            "order": 1,
            "is_featured": True
        },
        {
            "name": "Foundations",
            "slug": "foundations",
            "icon": "fa-magic",
            "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?q=80&w=800&auto=format&fit=crop",
            "description": "Flawless, second-skin liquid and cushion foundations with buildable coverage and luminous finishes.",
            "order": 2,
            "is_featured": True
        },
        {
            "name": "Concealers",
            "slug": "concealers",
            "icon": "fa-wand-magic-sparkles",
            "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?q=80&w=800&auto=format&fit=crop",
            "description": "Crease-resistant, high-coverage concealers to brighten eyes, camouflage blemishes, and sculpt contours.",
            "order": 3,
            "is_featured": True
        },
        {
            "name": "Blush",
            "slug": "blush",
            "icon": "fa-heart",
            "image_url": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=800&auto=format&fit=crop",
            "description": "Silky powder, cream, and liquid blushes that provide an authentic, lit-from-within flush.",
            "order": 4,
            "is_featured": True
        },
        {
            "name": "Highlighters",
            "slug": "highlighters",
            "icon": "fa-sun",
            "image_url": "https://images.unsplash.com/photo-1503236823255-94609f598e71?q=80&w=800&auto=format&fit=crop",
            "description": "Prismatic illuminators, baked highlighters, and dewy liquid drops for glass-skin brilliance.",
            "order": 5,
            "is_featured": True
        },
        {
            "name": "Eyeshadows",
            "slug": "eyeshadows",
            "icon": "fa-eye",
            "image_url": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?q=80&w=800&auto=format&fit=crop",
            "description": "Richly pigmented palettes featuring buttery mattes, sparkling duochromes, and molten metallics.",
            "order": 6,
            "is_featured": True
        },
        {
            "name": "Eyeliners",
            "slug": "eyeliners",
            "icon": "fa-pen-nib",
            "image_url": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?q=80&w=800&auto=format&fit=crop",
            "description": "Waterproof precision liquid felt-tip liners, gel pots, and smudgeable kohl pencils for arresting eye definition.",
            "order": 7,
            "is_featured": True
        },
        {
            "name": "Mascaras",
            "slug": "mascaras",
            "icon": "fa-feather",
            "image_url": "https://images.unsplash.com/photo-1591360236480-4ed861025fa1?q=80&w=800&auto=format&fit=crop",
            "description": "Volumizing, lengthening, and curling mascaras that coat each lash without clumping or flaking.",
            "order": 8,
            "is_featured": True
        },
        {
            "name": "Makeup Brushes",
            "slug": "makeup-brushes",
            "icon": "fa-paint-brush",
            "image_url": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?q=80&w=800&auto=format&fit=crop",
            "description": "Artisan-crafted vegan brushes with ultra-soft synthetic bristles and rose gold handles for seamless blending.",
            "order": 9,
            "is_featured": True
        },
        {
            "name": "Skincare",
            "slug": "skincare",
            "icon": "fa-spa",
            "image_url": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?q=80&w=800&auto=format&fit=crop",
            "description": "Nourishing hyaluronic serums, peptide creams, and revitalizing face oils that prep skin for flawless makeup.",
            "order": 10,
            "is_featured": True
        },
    ]

    cat_objs = {}
    for c in categories_data:
        cat_objs[c['slug']], _ = Category.objects.get_or_create(
            slug=c['slug'],
            defaults={
                'name': c['name'],
                'image_url': c['image_url'],
                'description': c['description'],
                'order': c['order'],
                'is_featured': c['is_featured'],
                'icon': c['icon']
            }
        )

    # 3. Create Realistic Sample Makeup Products
    print("Creating realistic luxury makeup products...")
    products_data = [
        # Lipsticks
        {
            "title": "Velvet Matte Luxe Lipstick",
            "slug": "velvet-matte-luxe-lipstick",
            "category": "lipsticks",
            "brand": "glow-glam-haute",
            "price": Decimal("32.00"),
            "original_price": Decimal("40.00"),
            "badge_text": "Bestseller",
            "is_featured": True,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("4.9"),
            "review_count": 184,
            "stock": 85,
            "short_description": "A weightless, long-wearing matte lipstick that delivers intense color payoff with a velvety soft-focus finish.",
            "description": "Indulge your lips in pure luxury. The Velvet Matte Luxe Lipstick combines ultra-saturated pure pigments with nourishing hyaluronic spheres and organic rosehip oil. It glides on effortlessly like silk, transforming into a transfer-resistant, feather-light matte veil that keeps lips cushion-soft for up to 16 hours without cracking.",
            "how_to_use": "Define lip borders with precision tip, then fill in starting from the center outward. Layer for heightened dramatic intensity.",
            "benefits": "• 16-hour transfer-resistant wear\n• Infused with Hyaluronic Acid & Vitamin E\n• Non-drying velvet finish\n• 100% Vegan & Cruelty-Free",
            "ingredients": "Dimethicone, Polyglyceryl-2 Triisostearate, Rosehip Seed Oil, Sodium Hyaluronate, Tocopherol (Vitamin E), Shea Butter, Iron Oxides.",
            "main_image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1625093742435-6fa192b6fb10?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "01 Rose Whisper", "color_hex": "#D87080"},
                {"name": "02 Nude Cashmere", "color_hex": "#BE7B6F"},
                {"name": "03 Scarlet Majesty", "color_hex": "#9B111E"},
                {"name": "04 Berry Romance", "color_hex": "#722F37"},
                {"name": "05 Sunset Terracotta", "color_hex": "#C35A48"}
            ]
        },
        {
            "title": "Satin Radiance Lip Nectar",
            "slug": "satin-radiance-lip-nectar",
            "category": "lipsticks",
            "brand": "velvet-rose-paris",
            "price": Decimal("28.00"),
            "original_price": Decimal("35.00"),
            "badge_text": "-20%",
            "is_featured": True,
            "is_bestseller": False,
            "is_new_arrival": True,
            "rating": Decimal("4.8"),
            "review_count": 92,
            "stock": 60,
            "short_description": "A glossy lip color enriched with French floral nectar that cushions lips with a high-shine plumped appearance.",
            "description": "Formulated in the heart of Paris, this conditioning lip nectar melts upon contact, delivering a mirror-like shine and lush color. Rose water extract and jojoba esters soothe fine lines for an irresistible pout.",
            "how_to_use": "Glide directly across bare lips or layer over lip pencil for high-dimensional glow.",
            "benefits": "• High-shine glossy finish\n• Plumping botanical formula\n• Hydration that lasts all day\n• Paraben-free & Non-sticky",
            "ingredients": "Hydrogenated Polyisobutene, Jojoba Oil, Rosa Damascena Extract, Peptides, Mica, Flavor.",
            "main_image": "https://images.unsplash.com/photo-1625093742435-6fa192b6fb10?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "01 Petal Dew", "color_hex": "#F08080"},
                {"name": "02 Caramel Glaze", "color_hex": "#C68E71"},
                {"name": "03 Peony Kiss", "color_hex": "#E06F85"}
            ]
        },

        # Foundations
        {
            "title": "Luminous Silk Perfection Foundation",
            "slug": "luminous-silk-perfection-foundation",
            "category": "foundations",
            "brand": "glow-glam-haute",
            "price": Decimal("48.00"),
            "original_price": Decimal("60.00"),
            "badge_text": "Bestseller",
            "is_featured": True,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("4.9"),
            "review_count": 312,
            "stock": 120,
            "short_description": "Award-winning liquid foundation that creates an undetectable, radiant second skin with 24-hour hydration.",
            "description": "The pinnacle of complexion artistry. Our Luminous Silk Foundation utilizes micro-fil technology to sculpt, brighten, and blur imperfections without ever looking cakey. Formulated with light-reflecting pearl particles, it mimics natural lit-from-within luminosity suitable for all skin types.",
            "how_to_use": "Dispense 1-2 pumps onto the back of the hand. Buff outward using our Rose Gold Foundation Brush or a damp sponge.",
            "benefits": "• Medium, buildable seamless coverage\n• 24-Hour dewy radiance\n• Sweat- and humidity-resistant\n• Non-comedogenic & dermatologist tested",
            "ingredients": "Aqua/Water, Cyclopentasiloxane, Glycerin, Dimethicone, Squalane, Niacinamide, Camellia Sinensis Leaf Extract, Silica.",
            "main_image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1608248597359-5f284e9c71e2?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "100 Fair Porcelain", "color_hex": "#FCE5D8"},
                {"name": "120 Warm Ivory", "color_hex": "#F6D2BD"},
                {"name": "210 Golden Beige", "color_hex": "#E6B89C"},
                {"name": "320 Honey Almond", "color_hex": "#C9916F"},
                {"name": "430 Rich Chestnut", "color_hex": "#8A5438"},
                {"name": "510 Deep Espresso", "color_hex": "#503022"}
            ]
        },
        {
            "title": "Pure Velvet Matte Foundation",
            "slug": "pure-velvet-matte-foundation",
            "category": "foundations",
            "brand": "nude-alchemy",
            "price": Decimal("44.00"),
            "original_price": None,
            "badge_text": "Clean Beauty",
            "is_featured": False,
            "is_bestseller": False,
            "is_new_arrival": True,
            "rating": Decimal("4.7"),
            "review_count": 68,
            "stock": 70,
            "short_description": "Oil-free matte foundation with pore-blurring zinc and niacinamide for all-day shine control.",
            "description": "Engineered for normal to oily skin, this weightless fluid controls sebum without draining moisture. Enriched with clean actives to soothe blemishes while maintaining a photo-ready velvet matte canvas.",
            "how_to_use": "Shake well before use. Apply in thin layers starting from the T-zone.",
            "benefits": "• 18-hour shine control\n• Formulated with Zinc & Niacinamide\n• Breathable, pore-refining finish",
            "ingredients": "Water, Isododecane, Zinc Oxide, Niacinamide, Dimethicone Crosspolymer, Salicylic Acid, Phenoxyethanol.",
            "main_image": "https://images.unsplash.com/photo-1608248597359-5f284e9c71e2?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Light Nude", "color_hex": "#F3D8C7"},
                {"name": "Medium Sand", "color_hex": "#D8A47F"},
                {"name": "Warm Bronze", "color_hex": "#A96E49"}
            ]
        },

        # Concealers
        {
            "title": "Radiant Camouflage Cream Concealer",
            "slug": "radiant-camouflage-cream-concealer",
            "category": "concealers",
            "brand": "glow-glam-haute",
            "price": Decimal("26.00"),
            "original_price": Decimal("32.00"),
            "badge_text": "Popular",
            "is_featured": True,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("4.8"),
            "review_count": 142,
            "stock": 95,
            "short_description": "An ultra-creamy, crease-proof concealer with caffeine and peptides that brightens dark circles instantly.",
            "description": "Say goodbye to tired eyes. This potent concealer blends skincare with pro-grade pigment. Caffeine de-puffs under-eyes, while botanical peptides visibly smooth fine lines and conceal redness seamlessly.",
            "how_to_use": "Dot under the eyes and on imperfections using the custom teardrop applicator. Tap with fingertip or beauty sponge.",
            "benefits": "• Crease-resistant formula\n• Infused with Caffeine & Peptides\n• 16-hour flexible wear",
            "ingredients": "Aqua, Caprylic/Capric Triglyceride, Glycerin, Caffeine, Palmitoyl Tripeptide-5, Hyaluronic Acid.",
            "main_image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Fair 01", "color_hex": "#FAE5D3"},
                {"name": "Light 02", "color_hex": "#F5CBA7"},
                {"name": "Medium 03", "color_hex": "#DC7633"},
                {"name": "Deep 04", "color_hex": "#873600"}
            ]
        },

        # Blush
        {
            "title": "Rose Petal Cushion Cream Blush",
            "slug": "rose-petal-cushion-cream-blush",
            "category": "blush",
            "brand": "petal-soft-london",
            "price": Decimal("24.00"),
            "original_price": Decimal("30.00"),
            "badge_text": "-20%",
            "is_featured": True,
            "is_bestseller": False,
            "is_new_arrival": True,
            "rating": Decimal("4.9"),
            "review_count": 87,
            "stock": 55,
            "short_description": "A dewy, melt-in cream blush infused with crushed rose petals that delivers a fresh youthful flush.",
            "description": "Capture that post-walk romantic glow. This breathable cream blush blends effortlessly with fingers or a brush, leaving a sheer, glass-like tint that never emphasizes skin texture.",
            "how_to_use": "Tap onto the apples of the cheeks and blend upwards toward the temples for a lifted effect.",
            "benefits": "• Dewy, glass-skin finish\n• Real crushed rose petals\n• Multi-use for cheeks and lips",
            "ingredients": "Squalane, Shea Butter, Rose Petal Powder, Tocopherol, Mica, Organic Jojoba Oil.",
            "main_image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "English Rose", "color_hex": "#E08D9D"},
                {"name": "Peach Bellini", "color_hex": "#F8A186"},
                {"name": "Berry Soufflé", "color_hex": "#BD5376"}
            ]
        },
        {
            "title": "Silk Radiance Baked Powder Blush",
            "slug": "silk-radiance-baked-powder-blush",
            "category": "blush",
            "brand": "glow-glam-haute",
            "price": Decimal("29.00"),
            "original_price": None,
            "badge_text": "Luxury Pick",
            "is_featured": False,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("4.8"),
            "review_count": 110,
            "stock": 45,
            "short_description": "Slow-baked Italian marble blush with luminous veins of champagne pearl for a multidimensional glow.",
            "description": "Baked on Italian terracotta tiles for 24 hours, this ultra-fine powder blush imparts a luminous, sculpted wash of color with zero chalkiness.",
            "how_to_use": "Swirl brush across the marbled dome and dust over cheekbones.",
            "benefits": "• Italian baked formulation\n• Micro-milled luminous pearls\n• 12-hour fade-proof wear",
            "ingredients": "Mica, Talc, Squalane, Dimethicone, Polysorbate 20, Phenoxyethanol.",
            "main_image": "https://images.unsplash.com/photo-1503236823255-94609f598e71?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Rosy Champagne", "color_hex": "#E29578"},
                {"name": "Golden Coral", "color_hex": "#F08080"}
            ]
        },

        # Highlighters
        {
            "title": "Celestial Starlight Pressed Highlighter",
            "slug": "celestial-starlight-pressed-highlighter",
            "category": "highlighters",
            "brand": "celestial-glow",
            "price": Decimal("34.00"),
            "original_price": Decimal("42.00"),
            "badge_text": "Must Have",
            "is_featured": True,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("5.0"),
            "review_count": 224,
            "stock": 90,
            "short_description": "A silky, diamond-dusted highlighter that captures the light with blinding, zero-glitter radiance.",
            "description": "Light up the room with pure celestial glow. Finely milled pearls melt into the skin for a wet-look sheen that accentuates your high points effortlessly. Flattering on all complexions.",
            "how_to_use": "Dust along cheekbones, brow bones, the bridge of the nose, and cupid's bow using a fan brush.",
            "benefits": "• High-impact, wet-look shine\n• Zero chunky glitter\n• Butter-soft texture",
            "ingredients": "Mica, Synthetic Fluorphlogopite, Dimethicone, Boron Nitride, Silica, Caprylyl Glycol.",
            "main_image": "https://images.unsplash.com/photo-1503236823255-94609f598e71?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "01 Moonlit Champagne", "color_hex": "#F7E7CE"},
                {"name": "02 Rose Gold Dust", "color_hex": "#ECC5C0"},
                {"name": "03 Sunburst Bronze", "color_hex": "#CD7F32"}
            ]
        },
        {
            "title": "Liquid Glass Drops Glow Illuminator",
            "slug": "liquid-glass-drops-glow-illuminator",
            "category": "highlighters",
            "brand": "glow-glam-haute",
            "price": Decimal("30.00"),
            "original_price": None,
            "badge_text": "New",
            "is_featured": False,
            "is_bestseller": False,
            "is_new_arrival": True,
            "rating": Decimal("4.8"),
            "review_count": 48,
            "stock": 65,
            "short_description": "Multipurpose liquid highlighter drops for custom all-over radiance or targeted gleaming accents.",
            "description": "Mix a drop into your foundation or moisturiser for all-over dewy perfection, or dab on high points for an ethereal glass skin reflection.",
            "how_to_use": "Apply 1-2 drops using the precision dropper and blend gently with fingertips.",
            "benefits": "• Mixable with skincare & foundations\n• Weightless fluid texture\n• Glass-like radiance",
            "ingredients": "Isododecane, Hydrogenated Polydecene, Squalane, Mica, Titanium Dioxide.",
            "main_image": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1503236823255-94609f598e71?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Pure Opal", "color_hex": "#FDFBF7"},
                {"name": "Golden Nectar", "color_hex": "#D4AF37"}
            ]
        },

        # Eyeshadows
        {
            "title": "Rose Gold Sunset Eyeshadow Palette",
            "slug": "rose-gold-sunset-eyeshadow-palette",
            "category": "eyeshadows",
            "brand": "glow-glam-haute",
            "price": Decimal("54.00"),
            "original_price": Decimal("68.00"),
            "badge_text": "Signature",
            "is_featured": True,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("4.9"),
            "review_count": 275,
            "stock": 80,
            "short_description": "14 sunset-inspired romantic shades in creamy velvety mattes, sparkling foil pearls, and molten metallics.",
            "description": "A collector's dream palette. Designed to take you from a soft daytime nude shimmer to an intoxicating evening smoky eye. Every shadow is enriched with softening emollients for effortless blending with zero fallout.",
            "how_to_use": "Build your base with warm transition shades, define crease with deeper hues, and press metallic foil onto center lids.",
            "benefits": "• 14 rich multidimensional shades\n• Velvety soft blendability\n• Zero fallout pigment technology\n• Deluxe mirror included",
            "ingredients": "Talc, Zinc Stearate, Dimethicone, Ethylhexyl Palmitate, Silica, Synthetic Sapphire.",
            "main_image": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1583241800698-e8ab01c85b27?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Golden Dawn (Foil)", "color_hex": "#FFD700"},
                {"name": "Dusk Rose (Matte)", "color_hex": "#C08081"},
                {"name": "Amber Bronze (Metallic)", "color_hex": "#CD7F32"}
            ]
        },
        {
            "title": "Nude Seduction Eyeshadow Quad",
            "slug": "nude-seduction-eyeshadow-quad",
            "category": "eyeshadows",
            "brand": "velvet-rose-paris",
            "price": Decimal("38.00"),
            "original_price": None,
            "badge_text": "Travel Pick",
            "is_featured": False,
            "is_bestseller": False,
            "is_new_arrival": True,
            "rating": Decimal("4.7"),
            "review_count": 54,
            "stock": 40,
            "short_description": "Four essential neutral shades curated for everyday French elegance and quick smoky eyes.",
            "description": "The ultimate everyday companion. Compact, sleek, and formulated with buttery soft minerals for instant chic eyes on the go.",
            "how_to_use": "Sweep lightest shade over lid, deepen socket with matte taupe, highlight inner corner with champagne.",
            "benefits": "• Compact travel-ready packaging\n• High color payoff in one swipe\n• Long-wear 12 hour formula",
            "ingredients": "Mica, Caprylic/Capric Triglyceride, Talc, Magnesium Stearate, Iron Oxides.",
            "main_image": "https://images.unsplash.com/photo-1583241800698-e8ab01c85b27?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Classic Nude Quad", "color_hex": "#B38B6D"}
            ]
        },

        # Eyeliners
        {
            "title": "Precision Ink Waterproof Liquid Eyeliner",
            "slug": "precision-ink-waterproof-liquid-eyeliner",
            "category": "eyeliners",
            "brand": "glow-glam-haute",
            "price": Decimal("22.00"),
            "original_price": Decimal("26.00"),
            "badge_text": "24H Wear",
            "is_featured": True,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("4.9"),
            "review_count": 190,
            "stock": 110,
            "short_description": "An ultra-fine 0.1mm calligraphy tip eyeliner that delivers pitch-black, smudge-proof lines for 24 hours.",
            "description": "Master the winged liner with zero hesitation. The ergonomic handle and flexible Japanese brush tip allow you to draw sharp micro-lines or dramatic graphic sweeps. Waterproof, tear-proof, and humidity-resistant.",
            "how_to_use": "Shake gently. Glide tip along lash line from inner corner toward temple.",
            "benefits": "• Ultra-precise 0.1mm brush tip\n• 24-Hour smudge-proof & waterproof\n• Pitch carbon-black pigment",
            "ingredients": "Water, Acrylates Copolymer, Carbon Black, Butylene Glycol, Laureth-21, Phenoxyethanol.",
            "main_image": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1591360236480-4ed861025fa1?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Midnight Carbon Black", "color_hex": "#0F0F0F"},
                {"name": "Espresso Velvet Brown", "color_hex": "#382212"}
            ]
        },

        # Mascaras
        {
            "title": "Infinity Lash Drama & Volume Mascara",
            "slug": "infinity-lash-drama-volume-mascara",
            "category": "mascaras",
            "brand": "glow-glam-haute",
            "price": Decimal("26.00"),
            "original_price": Decimal("32.00"),
            "badge_text": "Bestseller",
            "is_featured": True,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("4.8"),
            "review_count": 210,
            "stock": 130,
            "short_description": "Dramatic false-lash effect mascara with an hourglass wand that lifts, separates, and volumizes tenfold.",
            "description": "Unlock instant volume and panoramic lash lift. Our peptide-infused lash-loving formula conditions hairs while building dramatic black volume without clumping or flaking throughout the day.",
            "how_to_use": "Wiggle brush from lash roots to tips in an upward sweeping motion. Layer 2-3 coats for full drama.",
            "benefits": "• Dramatic 10x volume boost\n• Nourishing peptide & castor oil blend\n• Zero flake, zero clump formula",
            "ingredients": "Aqua, Cera Alba (Beeswax), Castor Seed Oil, Biotinoyl Tripeptide-1, Iron Oxides.",
            "main_image": "https://images.unsplash.com/photo-1591360236480-4ed861025fa1?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Ultra Intense Black", "color_hex": "#111111"}
            ]
        },

        # Makeup Brushes
        {
            "title": "Rose Gold 10-Piece Luxury Artisan Brush Set",
            "slug": "rose-gold-10-piece-luxury-artisan-brush-set",
            "category": "makeup-brushes",
            "brand": "glow-glam-haute",
            "price": Decimal("65.00"),
            "original_price": Decimal("85.00"),
            "badge_text": "-24%",
            "is_featured": True,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("5.0"),
            "review_count": 340,
            "stock": 50,
            "short_description": "Handcrafted cruelty-free brushes with ultra-plush cashmere-soft synthetic bristles in a designer roll case.",
            "description": "The quintessential set for beauty connoisseurs. Contains 10 essential face and eye brushes tailored with rose gold ferrules and weighted wooden handles. Blends powders, creams, and liquids like air.",
            "how_to_use": "Use specialized brushes for foundation, contour, blush, powder, highlighter, crease blending, and detailing.",
            "benefits": "• 10 full-sized pro brushes\n• 100% Vegan Dermocura bristles\n• Includes plush rose gold travel clutch\n• Shed-proof durability",
            "ingredients": "Dermocura Synthetic Fibers, Aluminum Ferrule, Certified Sustainable Birch Wood.",
            "main_image": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Rose Gold & Nude Set", "color_hex": "#C88A83"}
            ]
        },
        {
            "title": "Velvet Sculpt & Contour Buffer Brush",
            "slug": "velvet-sculpt-contour-buffer-brush",
            "category": "makeup-brushes",
            "brand": "petal-soft-london",
            "price": Decimal("22.00"),
            "original_price": None,
            "badge_text": "Pro Tool",
            "is_featured": False,
            "is_bestseller": False,
            "is_new_arrival": True,
            "rating": Decimal("4.9"),
            "review_count": 45,
            "stock": 60,
            "short_description": "Angled kabuki buffer brush designed to hug facial curves for razor-sharp cheekbone contouring.",
            "description": "Engineered with dense, silky angled bristles that effortlessly buff cream and powder contour into hollows of cheeks and jawline.",
            "how_to_use": "Stamp contour along jawline and under cheekbones, then buff upward in circular motions.",
            "benefits": "• Angled chisel shape\n• Zero bristle shedding\n• Flawless streak-free blending",
            "ingredients": "Ultra-fine synthetic fiber, rose gold ferrule.",
            "main_image": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Chiseled Rose", "color_hex": "#B76E79"}
            ]
        },

        # Skincare
        {
            "title": "Dewy Radiance 24K Gold Elixir Face Oil",
            "slug": "dewy-radiance-24k-gold-elixir-face-oil",
            "category": "skincare",
            "brand": "lumiere-botanicals",
            "price": Decimal("58.00"),
            "original_price": Decimal("75.00"),
            "badge_text": "Clean Luxury",
            "is_featured": True,
            "is_bestseller": True,
            "is_new_arrival": False,
            "rating": Decimal("4.9"),
            "review_count": 160,
            "stock": 75,
            "short_description": "A rejuvenating youth elixir infused with pure 24-karat gold flakes and 9 cold-pressed organic botanicals.",
            "description": "The ultimate ritual for sublime radiance. Micro-particles of 24K pure gold absorb effortlessly, stimulating cellular turnover while rosehip, marula, and camellia oils deeply nourish the skin barrier.",
            "how_to_use": "Warm 3 drops between palms and gently press into freshly cleansed face and neck before makeup application.",
            "benefits": "• Pure 24K gold illumination\n• 9 Cold-pressed organic face oils\n• Instant dewy glow with zero greasy feel\n• Strengthens skin moisture barrier",
            "ingredients": "Rosa Canina (Rosehip) Seed Oil, Camellia Japonica Seed Oil, Sclerocarya Birrea (Marula) Kernel Oil, 24K Gold Leaf, Frankincense Oil.",
            "main_image": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "24K Gold Pure Elixir", "color_hex": "#FFD700"}
            ]
        },
        {
            "title": "Hydra-Glow Hyaluronic Plumping Serum",
            "slug": "hydra-glow-hyaluronic-plumping-serum",
            "category": "skincare",
            "brand": "lumiere-botanicals",
            "price": Decimal("46.00"),
            "original_price": Decimal("55.00"),
            "badge_text": "New",
            "is_featured": True,
            "is_bestseller": False,
            "is_new_arrival": True,
            "rating": Decimal("4.8"),
            "review_count": 82,
            "stock": 80,
            "short_description": "Multi-molecular hyaluronic acid serum that floods skin with intense hydration for a bouncy glass-like appearance.",
            "description": "Quench thirsty skin. With 5 molecular weights of hyaluronic acid and provitamin B5, this serum penetrates multiple layers of skin to smooth texture and create the perfect plump base for makeup.",
            "how_to_use": "Apply 3-4 drops onto damp skin morning and night followed by your favorite cream.",
            "benefits": "• 5 Molecular weights of Hyaluronic Acid\n• Bouncy, glass-skin hydration\n• Calms irritation with Panthenol (B5)",
            "ingredients": "Aqua, Sodium Hyaluronate, Panthenol, Glycerin, Centella Asiatica Extract, Allantoin.",
            "main_image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?q=80&w=800&auto=format&fit=crop",
            "hover_image": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?q=80&w=800&auto=format&fit=crop",
            "shades": [
                {"name": "Hydra Glow Serum", "color_hex": "#E0FFFF"}
            ]
        }
    ]

    for p in products_data:
        cat = cat_objs[p['category']]
        brand = brand_objs[p['brand']]
        prod = Product.objects.create(
            title=p['title'],
            slug=p['slug'],
            category=cat,
            brand=brand,
            price=p['price'],
            original_price=p['original_price'],
            badge_text=p['badge_text'],
            is_featured=p['is_featured'],
            is_bestseller=p['is_bestseller'],
            is_new_arrival=p['is_new_arrival'],
            rating=p['rating'],
            review_count=p['review_count'],
            stock=p['stock'],
            short_description=p['short_description'],
            description=p['description'],
            how_to_use=p['how_to_use'],
            benefits=p['benefits'],
            ingredients=p['ingredients'],
            main_image=p['main_image'],
            hover_image=p['hover_image']
        )

        # Additional gallery images
        ProductImage.objects.create(product=prod, image_url=p['hover_image'], alt_text=f"{prod.title} detail view")
        ProductImage.objects.create(product=prod, image_url=p['main_image'], alt_text=f"{prod.title} front view")

        # Create Shades
        for s in p.get('shades', []):
            ProductShade.objects.create(
                product=prod,
                name=s['name'],
                color_hex=s['color_hex'],
                in_stock=True
            )

        # Create realistic customer reviews
        sample_reviews = [
            {
                "author_name": "Eleanor Vance",
                "rating": 5,
                "title": "Absolute luxury in a bottle!",
                "comment": "This has completely transformed my daily beauty routine. The formula is so buttery and lightweight, and it lasts through dinner without a touch-up. Worth every single penny!"
            },
            {
                "author_name": "Camille Dupont",
                "rating": 5,
                "title": "Obsessed with the packaging and finish",
                "comment": "The rose gold heavy casing feels like something out of a Parisian boutique. And the texture on the skin is divine. I get compliments everywhere I go."
            },
            {
                "author_name": "Maya Patel",
                "rating": 4,
                "title": "Beautiful color payoff",
                "comment": "Rich pigments and very hydrating. I love that it doesn't settle into fine lines. Giving it 4.8 stars because I want more nude tones!"
            }
        ]
        for rev in sample_reviews:
            Review.objects.create(
                product=prod,
                author_name=rev['author_name'],
                rating=rev['rating'],
                title=rev['title'],
                comment=rev['comment'],
                verified=True
            )

    # 4. Create Active Coupons
    print("Creating promotional coupons...")
    coupons = [
        {"code": "GLAM20", "discount_percent": 20, "discount_amount": Decimal("0.00"), "min_order_amount": Decimal("0.00")},
        {"code": "GLOW10", "discount_percent": 10, "discount_amount": Decimal("0.00"), "min_order_amount": Decimal("0.00")},
        {"code": "BEAUTY15", "discount_percent": 15, "discount_amount": Decimal("0.00"), "min_order_amount": Decimal("40.00")},
        {"code": "FREESHIP", "discount_percent": 0, "discount_amount": Decimal("5.00"), "min_order_amount": Decimal("20.00")},
    ]
    for c in coupons:
        Coupon.objects.get_or_create(code=c['code'], defaults=c)

    # 5. Create Demo Admin and Customer
    print("Creating demo users...")
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@glowandglam.com', 'admin123')
        admin_user.first_name = "Admin"
        admin_user.last_name = "Manager"
        admin_user.save()
        print("Created superuser: admin / admin123")

    demo_user, created = User.objects.get_or_create(username='sophia', defaults={
        'email': 'sophia.laurent@example.com',
        'first_name': 'Sophia',
        'last_name': 'Laurent'
    })
    if created:
        demo_user.set_password('glam123')
        demo_user.save()
        profile = demo_user.profile
        profile.phone = "+1 (555) 789-2341"
        profile.address = "450 Fifth Avenue, Suite 1200"
        profile.city = "New York"
        profile.state = "NY"
        profile.postal_code = "10018"
        profile.skin_type = "Radiant / Combination"
        profile.favorite_category = "Lipsticks"
        profile.save()

        # Create demo order for Sophia so Order History has data!
        sample_prod = Product.objects.filter(slug='velvet-matte-luxe-lipstick').first()
        sample_prod2 = Product.objects.filter(slug='luminous-silk-perfection-foundation').first()

        order = Order.objects.create(
            user=demo_user,
            full_name="Sophia Laurent",
            email="sophia.laurent@example.com",
            phone="+1 (555) 789-2341",
            address="450 Fifth Avenue, Suite 1200",
            city="New York",
            state="NY",
            postal_code="10018",
            shipping_method="Standard Delivery",
            shipping_cost=Decimal("0.00"),
            payment_method="card",
            payment_status="Paid (Demo)",
            subtotal=Decimal("80.00"),
            discount_amount=Decimal("16.00"),
            tax_amount=Decimal("3.20"),
            total_price=Decimal("67.20"),
            status="Shipped"
        )
        if sample_prod:
            OrderItem.objects.create(
                order=order,
                product=sample_prod,
                product_title=sample_prod.title,
                product_image=sample_prod.main_image,
                shade_name="01 Rose Whisper",
                price=sample_prod.price,
                quantity=1
            )
        if sample_prod2:
            OrderItem.objects.create(
                order=order,
                product=sample_prod2,
                product_title=sample_prod2.title,
                product_image=sample_prod2.main_image,
                shade_name="120 Warm Ivory",
                price=sample_prod2.price,
                quantity=1
            )
        print("Created demo user: sophia / glam123 with sample order!")

    print(f"Successfully seeded database! Total categories: {Category.objects.count()}, Total products: {Product.objects.count()}")

if __name__ == '__main__':
    seed()
