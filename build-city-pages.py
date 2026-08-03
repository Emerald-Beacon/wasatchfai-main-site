#!/usr/bin/env python3
"""
Generate city/service-area pages for Wasatch Foot & Ankle Institute.

Chrome (topbar, header, footer, call bar) is lifted verbatim from
farmington-utah.html so these pages can never drift from the rest of the site.
Everything inside the content region is authored per city in CITIES below.

WHY SO MUCH PER-CITY COPY: a first pass that shared the FAQ block, the
same-day paragraph and the insurance paragraph across all 11 pages measured
only 37% pairwise uniqueness -- i.e. the pages were 63% identical to each
other, which is the classic doorway-page signature Google penalises. The
fields below (local_1..local_3, activity_body, same_day, insurance_note,
conditions_intro, faqs_local) exist to push that above 60%. build_and_check()
enforces the floor at generation time; if you add a city and the floor fails,
the script exits non-zero rather than writing thin pages.

Positioning: the two CLINIC pages (farmington-utah.html,
ogden-utah-foot-doctor.html) own address/NAP intent. These CITY pages own
"podiatrist in <city>" intent and funnel to the nearest clinic.

Run from the repo root:  python3 build-city-pages.py
"""
import re
import sys
import json
import html as _html
import itertools
import pathlib
import statistics

ROOT = pathlib.Path(__file__).parent
SRC = (ROOT / "farmington-utah.html").read_text(encoding="utf-8")

UNIQUENESS_FLOOR = 0.60

# ---------------------------------------------------------------- chrome ----
_h = SRC.index("<!-- TOP BAR -->")
TOPBAR_HEADER = SRC[_h:SRC.index("</header>", _h) + len("</header>")]
_f = SRC.index("<!-- FOOTER -->")
FOOTER = SRC[_f:SRC.index("</footer>", _f) + len("</footer>")]
_cb = SRC.index("<!-- MOBILE CALL BAR -->")
CALLBAR = SRC[_cb:SRC.index("</nav>", _cb) + len("</nav>")]

# --------------------------------------------------------------- clinics ----
CLINICS = {
    "farmington": {
        "name": "Farmington", "page": "farmington-utah.html",
        "street": "473 W. Bourne Circle, Suite 2", "city": "Farmington", "zip": "84025",
        "phone": "801-451-7500", "tel": "8014517500", "e164": "+1-801-451-7500",
        "map_q": "473+W+Bourne+Circle+Suite+2+Farmington+UT+84025",
        "lat": 40.9869, "lon": -111.9066, "county": "Davis County",
    },
    "ogden": {
        "name": "South Ogden", "page": "ogden-utah-foot-doctor.html",
        "street": "945 Chambers Street, Suite 3", "city": "South Ogden", "zip": "84403",
        "phone": "801-627-2122", "tel": "8016272122", "e164": "+1-801-627-2122",
        "map_q": "945+Chambers+Street+Suite+3+South+Ogden+UT+84403",
        "lat": 41.1725, "lon": -111.9580, "county": "Weber County",
    },
}

# ----------------------------------------------------------------- cities ----
CITIES = [
{
 "slug":"kaysville-utah","city":"Kaysville","zip":"84037","clinic":"farmington","county":"Davis County",
 "neighbors":"Fruit Heights, Layton, Farmington, and the east bench",
 "drive":"about 10 minutes",
 "route":"Head south on Main Street to US-89, or take I-15 south to Exit 325 (Park Lane). Either route is roughly ten minutes outside of rush hour.",
 "lede":"Kaysville patients are about ten minutes from our Farmington clinic &mdash; close enough that a same-day appointment for a rolled ankle or an infected ingrown toenail rarely costs more than a lunch break.",
 "local_1":"Kaysville sits between the Wasatch bench and the interstate, and that geography shows up in the feet we see. Patients coming down off the East Mountain Wilderness Park trails and the Baer Creek drainage arrive with ankle sprains, Achilles complaints, and the forefoot pain that follows a long descent. Patients who spend the day on the flats &mdash; commuting to Salt Lake or Ogden, standing at work &mdash; are far more likely to present with heel pain that is worst on the first step out of bed.",
 "local_2":"We also see a steady stream of Davis High and Kaysville Junior families through the school sports seasons. Growth-plate injuries, calcaneal apophysitis in younger athletes, and repeat ankle sprains in kids who never fully rehabilitated the first one are all common here, and all worth evaluating rather than waiting out.",
 "local_3":"Winter changes the pattern again. Kaysville&rsquo;s older neighbourhoods east of Main have steep driveways and long north-facing walks that hold ice well into February, and slip-and-fall ankle fractures climb sharply in January. If you go down on ice and cannot bear weight for more than a few steps, that needs an X-ray rather than a wait-and-see week &mdash; ankle fractures that are walked on for a fortnight are considerably harder to fix well.",
 "activity":"The bench trails, the commute, and the school-sports calendar",
 "activity_body":"If you hike or trail-run the benches above Kaysville, it is the descent that hurts you rather than the climb. Steep, loose downhill loads the Achilles and the plantar fascia hard, and it is the single most common mechanism behind the heel pain we treat in Davis County. If you commute and stand all day instead, the mechanism is different but the diagnosis is frequently the same &mdash; and so is the fix.",
 "conditions_intro":"Kaysville patients most often come to us with heel pain, bench-trail ankle sprains, and youth sports injuries. We treat all of it, along with the full range of foot and ankle problems:",
 "same_day":"Kaysville is close enough that same-day care is genuinely practical rather than theoretical. If an athlete rolls an ankle at Friday practice, or a toenail turns red and hot over the weekend, call first thing and we will try to see you that morning rather than the following week.",
 "insurance_note":"A large share of Kaysville families are covered through PEHP or the Davis School District plans, and we work with both. Call and our team will confirm your benefits before you come in.",
 "faqs_local":[
   ("How far is your clinic from Kaysville?","Our Farmington clinic is about ten minutes from central Kaysville. Take Main Street south to US-89, or I-15 south to Exit 325 (Park Lane). There is free surface parking directly outside the building."),
   ("Do you treat high school and junior high athletes?","Yes, and we see a lot of them from the Davis High and Kaysville Junior programmes. Ankle sprains, heel pain during growth spurts, and stress reactions from a sudden jump in training load are the three we see most. Adolescent heel pain in particular is often the growth plate rather than tendonitis, and it needs a different plan than an adult heel."),
   ("My child&rsquo;s heel hurts during a growth spurt &mdash; is that normal?","It is common, but it is not something to simply endure. Pain at the back of the heel in a growing athlete usually points to irritation of the growth plate, which settles reliably with the right activity modification, footwear, and stretching. It is worth confirming the diagnosis rather than assuming, because a stress fracture can look similar early on."),
 ]},
{
 "slug":"fruit-heights-utah","city":"Fruit Heights","zip":"84037","clinic":"farmington","county":"Davis County",
 "neighbors":"Kaysville, Farmington, and the Baer Canyon bench",
 "drive":"about 8 minutes",
 "route":"Come down the hill to US-89 and head south, or take Nicholls Road across to Main Street. It is a short, simple drive &mdash; roughly eight minutes door to door.",
 "lede":"Fruit Heights is one of the closest communities to our Farmington clinic &mdash; a straight eight-minute run down US-89 &mdash; which makes it practical to be seen the same day rather than waiting out a foot problem.",
 "local_1":"Fruit Heights is small, residential, and pressed right up against the mountain, and the Baer Canyon trailhead at the top of town explains much of what we treat here. Baer is steep and rocky from the first quarter mile. Ankle inversion sprains, midfoot bruising, and Achilles tendonitis are the predictable results, particularly in hikers who go up hard in the spring after a sedentary winter.",
 "local_2":"The other half of what we see is ordinary and no less worth treating: bunions that have finally started to hurt rather than merely look wrong, toenails that keep growing in, and arthritis in the big toe joint that makes the last stretch of a walk miserable. Living at the base of a canyon exempts nobody from the everyday problems.",
 "local_3":"Because Fruit Heights is a small city with no clinic of its own, most residents are used to driving somewhere for care. The advantage of being eight minutes out is that follow-up stops being a burden &mdash; and foot and ankle care is unusually follow-up dependent. Post-operative checks, cast and boot changes, wound reviews, and orthotic fittings all work far better when the drive is trivial.",
 "activity":"Baer Canyon and the Fruit Heights bench",
 "activity_body":"Steep-canyon hiking is hard on the back of the heel and the outside of the ankle. If you have rolled the same ankle more than twice, that is not bad luck &mdash; it usually means a ligament healed long and the joint is now loose enough to give way on uneven ground. That is a treatable mechanical problem, not something to keep taping indefinitely.",
 "conditions_intro":"Canyon hikers from Fruit Heights bring us ankle instability and Achilles problems; everyone else brings the ordinary complaints that respond just as well to treatment:",
 "same_day":"An eight-minute drive means an urgent problem does not have to wait. Infected ingrown toenails, sudden severe heel pain, and suspected fractures are the three we most often fit in the same day for Fruit Heights patients.",
 "insurance_note":"We accept nearly all major carriers used across Davis County. If you have recently changed plans through an employer in Salt Lake or Ogden, call ahead and we will verify in-network status before your visit.",
 "faqs_local":[
   ("How far is your clinic from Fruit Heights?","About eight minutes. Take US-89 south from Fruit Heights toward Farmington and exit at Park Lane. The clinic is at 473 W. Bourne Circle, Suite 2, with free parking outside the door."),
   ("I keep rolling the same ankle on the Baer Canyon trail. Is that fixable?","Usually, yes. Repeated sprains on the same ankle normally mean the ligament healed in a lengthened position, leaving the joint mechanically unstable. Bracing and targeted rehabilitation resolve many cases; when they do not, ligament reconstruction is a well-established procedure with good outcomes. See our page on <a href=\"lateral-ankle-instability.html\">lateral ankle instability</a>."),
   ("Do I need to be referred by my family doctor?","In most cases, no. Patients can book directly with us. A minority of insurance plans require a referral for specialist care, so it is worth a quick call to your insurer if you are unsure &mdash; or call us and we will check for you."),
 ]},
{
 "slug":"centerville-utah","city":"Centerville","zip":"84014","clinic":"farmington","county":"Davis County",
 "neighbors":"Farmington, Bountiful, and West Bountiful",
 "drive":"about 7 minutes",
 "route":"Take I-15 north one exit to Exit 325 (Park Lane), or stay on the frontage road and follow it north.",
 "lede":"Centerville is our nearest neighbour &mdash; roughly seven minutes up the frontage road or one exit north on I-15 &mdash; which makes our Farmington clinic the practical choice for anything needing more than a single visit.",
 "local_1":"Two very different Centerville habits drive most of what we treat. The Deuel Creek trails and the canyon routes above town are steep and rocky, and they produce ankle sprains and Achilles pain. The Legacy Parkway Trail is the opposite &mdash; flat, paved, and long &mdash; and it produces overuse injuries that come from high mileage on hard, unvarying ground: plantar fasciitis, metatarsal stress reactions, and neuromas.",
 "local_2":"If you have recently increased mileage on the Legacy trail and developed a deep ache in the ball of the foot that worsens through a run and eases with rest, that deserves imaging rather than blind rest. Metatarsal stress fractures are easy to miss early and expensive to miss late, and the difference between a six-week boot and a much longer recovery is often just how quickly it was identified.",
 "local_3":"Centerville also has a large share of residents who commute south to Salt Lake and spend the day seated, then try to compress a week&rsquo;s activity into the weekend. That pattern &mdash; five sedentary days, two hard ones &mdash; is one of the more reliable ways to develop plantar fasciitis and Achilles tendonitis, because the tissue never builds tolerance for the load it is suddenly asked to absorb.",
 "activity":"The Legacy Parkway Trail and the Deuel Creek benches",
 "activity_body":"Flat paved mileage and steep dirt descents injure feet in opposite ways. Paved repetition concentrates load through the same tissues every stride, which favours plantar fasciitis and stress reactions. Rocky descent asks the ankle to stabilise on an unpredictable surface, which favours sprains. We treat both, and the distinction genuinely changes the plan.",
 "conditions_intro":"Centerville brings us a fairly even split of trail injuries and paved-mileage overuse problems, alongside everything else we treat:",
 "same_day":"At seven minutes away, Centerville patients get the most practical access to our same-day slots of anyone outside Farmington itself. Call early in the day for fractures, wounds, and sudden severe pain.",
 "insurance_note":"Many Centerville patients commute to Salt Lake employers and carry plans administered out of the valley. We are in-network with most; a quick call before your visit removes any doubt.",
 "faqs_local":[
   ("How far is your clinic from Centerville?","About seven minutes. Centerville is one exit south of the clinic &mdash; take I-15 north to Exit 325 (Park Lane), or follow the frontage road north. Parking is free and directly outside."),
   ("I run the Legacy Parkway Trail and my forefoot aches. What is that?","Deep forefoot pain that builds through a run and settles with rest is most often a metatarsal stress reaction, a neuroma, or plain metatarsalgia from load and footwear. They are treated quite differently, so it is worth identifying which one you have before changing your training. Stress reactions in particular respond badly to running through them."),
   ("Do you make custom orthotics for runners?","Yes. Runners are one of the groups who benefit most, because a device can be built for the specific mechanics causing the problem rather than sold off a shelf. See <a href=\"custom-orthotics.html\">custom orthotics</a> for how the process works and what to expect."),
 ]},
{
 "slug":"bountiful-utah","city":"Bountiful","zip":"84010","clinic":"farmington","county":"Davis County",
 "neighbors":"West Bountiful, Woods Cross, North Salt Lake, and Centerville",
 "drive":"about 13 minutes",
 "route":"I-15 north to Exit 325 (Park Lane) is fastest from most of Bountiful. From the east bench, 400 North to US-89 north avoids the freeway entirely.",
 "lede":"Bountiful is about thirteen minutes south of our Farmington clinic, and we treat a large share of the Mueller Park and Bountiful bench crowd &mdash; hikers, trail runners, and cyclists who need feet that hold up on steep ground.",
 "local_1":"Mueller Park Trail is the most-used trailhead in south Davis County, and it shows in our schedule. The climb toward Elephant Rock is long and steady; the descent is where ankles roll and Achilles tendons complain. There is a predictable spring surge in these injuries as the snow line moves up and people return to the trail without rebuilding tolerance first.",
 "local_2":"Bountiful also has an older, well-established population, and a good portion of our work here is arthritis of the big toe joint, bunion deformity that has become painful rather than merely visible, and diabetic foot care. That last category matters most: a diabetic foot ulcer caught in week one is a wound-care problem, and the same ulcer caught in month three can become a limb problem.",
 "local_3":"The Bountiful bench adds a mechanical wrinkle that patients rarely think about. Long walks and rides on steeply cambered roads load one foot differently from the other for the entire outing, and asymmetric load produces asymmetric injury. When someone tells us only the left heel hurts and they walk the same bench loop daily in the same direction, the camber is usually part of the answer.",
 "activity":"Mueller Park, the Bountiful bench, and the golf-course crowd",
 "activity_body":"Long steady climbs load the calf and Achilles; long steady descents load the heel and forefoot. Bountiful Ridge and the bench roads add a lot of miles on cambered pavement, which quietly aggravates one side more than the other. If one foot hurts and the other does not, that asymmetry is usually the clue worth chasing.",
 "conditions_intro":"Bountiful sends us trail injuries from Mueller Park and a steady volume of arthritis, bunion, and diabetic foot care. We treat the full range:",
 "same_day":"Same-day slots matter most here for diabetic patients. If you have diabetes and notice a new blister, a colour change, drainage, or any wound that has not begun healing within a few days, treat that as urgent and call &mdash; do not wait for your next routine appointment.",
 "insurance_note":"We accept Medicare along with nearly all major commercial carriers, which matters for a good share of our Bountiful patients. Diabetic shoe and orthotic benefits vary by plan, and our team can tell you what yours covers.",
 "faqs_local":[
   ("How far is your clinic from Bountiful?","About thirteen minutes. Take I-15 north to Exit 325 (Park Lane). From the Bountiful bench, 400 North to US-89 north is a good freeway-free alternative. Free parking is available outside the clinic."),
   ("I have diabetes. How often should my feet be checked?","At least once a year as a formal examination, and daily by you at home. If you have any numbness, a previous ulcer, or reduced circulation, more frequent professional checks are appropriate. Neuropathy removes the pain signal that would normally warn you, so the wounds that matter most are often the ones that never hurt. See <a href=\"diabetic-foot-care-1.html\">diabetic foot care</a>."),
   ("My bunion has started hurting after years of being painless. What changed?","Usually the joint, not the bump. Bunions progress slowly, and pain often begins when the big toe joint starts to lose motion or when the deformity shifts load onto the neighbouring metatarsals. That is worth assessing, because the treatment differs depending on whether the problem is pressure from footwear or arthritis inside the joint. See <a href=\"bunion-removal.html\">bunion treatment</a>."),
 ]},
{
 "slug":"woods-cross-utah","city":"Woods Cross","zip":"84087","clinic":"farmington","county":"Davis County",
 "neighbors":"West Bountiful, Bountiful, and North Salt Lake",
 "drive":"about 12 minutes",
 "route":"Legacy Parkway north to I-15, then Exit 325 (Park Lane). From central Woods Cross the trip is usually inside a quarter of an hour.",
 "lede":"Woods Cross sits about twelve minutes south of our Farmington clinic via Legacy Parkway, and a large share of the feet we treat here belong to people who stand on concrete for a living.",
 "local_1":"Woods Cross is an industrial and logistics town as much as a residential one. Refinery work, warehouse work, and rail work all mean long shifts on unforgiving surfaces in stiff safety boots &mdash; a combination that produces heel pain, metatarsalgia, and nail problems from boots half a size too small. Steel-toe footwear in particular is a common and under-appreciated cause of ingrown toenails and bruised nail beds.",
 "local_2":"If your feet hurt worst in the first hour of a shift and again in the first steps after sitting down, that pattern points strongly toward plantar fasciitis, and it responds well to treatment. Working through it for a year does not resolve it; it usually makes the heel more sensitive and the eventual recovery longer.",
 "local_3":"Shift patterns matter clinically, not just logistically. A body on nights, or on rotating twelve-hour shifts, gets less consistent rest for healing tissue and tends to compress errands and exercise into unpredictable windows. When we build a treatment plan for a Woods Cross shift worker we plan around the roster rather than pretending it does not exist &mdash; because a plan that requires resting during working hours is a plan nobody follows.",
 "activity":"Shift work, safety boots, and the Legacy Parkway Trail",
 "activity_body":"Occupational foot pain is genuinely different from athletic foot pain. The load is lower but nearly continuous, the footwear is chosen for protection rather than fit, and there is no rest day. Orthotics built to fit inside a work boot &mdash; rather than a running shoe &mdash; make a real difference here, and so does getting the boot size right in the first place.",
 "conditions_intro":"Occupational foot problems dominate what we see from Woods Cross, but we treat the full range of foot and ankle conditions:",
 "same_day":"Industrial injuries do not schedule themselves. Crush injuries to the toes, puncture wounds, and suspected fractures should be seen the same day &mdash; call as soon as it happens rather than finishing the shift and hoping.",
 "insurance_note":"Workers&rsquo; compensation cases are common from the Woods Cross industrial corridor, and our team is experienced in handling the documentation. Bring your claim number and employer details to the first visit if the injury happened at work.",
 "faqs_local":[
   ("How far is your clinic from Woods Cross?","About twelve minutes. Take Legacy Parkway north to I-15 and exit at 325 (Park Lane). The clinic is at 473 W. Bourne Circle, Suite 2, with free ground-level parking."),
   ("Can you make orthotics that fit inside steel-toe work boots?","Yes, and this is a common request here. Work-boot orthotics have to be built differently &mdash; a lower-volume device with a different shell and top cover, because a safety boot has far less internal room than a trainer. Bring the actual boots you wear to your appointment so the fit can be checked properly."),
   ("My foot injury happened at work. Do you handle workers&rsquo; compensation?","Yes. Bring your claim number, your employer&rsquo;s details, and the date of injury to your first visit. If the claim has not been filed yet, let our front desk know at check-in so the visit is documented correctly from the start."),
 ]},
{
 "slug":"layton-utah","city":"Layton","zip":"84041","clinic":"farmington","county":"Davis County",
 "neighbors":"Kaysville, Clearfield, Syracuse, and Hill Air Force Base",
 "drive":"about 12 minutes",
 "route":"I-15 south to Exit 325 (Park Lane) is fastest from anywhere in Layton. From the east side of town, US-89 south is often quicker in the afternoon.",
 "lede":"Layton is about twelve minutes north of our Farmington clinic, and between Hill Air Force Base, Adams Canyon, and a large youth-sports population it sends us as varied a mix of foot and ankle problems as any city in Davis County.",
 "local_1":"Adams Canyon deserves specific mention. It is short, relentlessly steep, and loose underfoot, and it is responsible for a disproportionate share of the ankle sprains and Achilles injuries we treat from Layton. The waterfall turnaround tempts people into a fast descent on tired legs, which is precisely when ankles give way.",
 "local_2":"The Hill Air Force Base workforce brings a different pattern &mdash; long shifts, mandated footwear, and fitness standards that must be met regardless of how the feet feel. We see a lot of stress reactions in that group, along with heel pain that has been managed with over-the-counter inserts for far too long before anyone looked at it properly.",
 "local_3":"Layton&rsquo;s size works against early treatment in one specific way: there is enough retail, enough urgent care, and enough general practice in town that foot problems get triaged repeatedly without ever reaching someone who treats feet all day. We regularly meet patients on their third or fourth attempt at the same heel pain. If two rounds of generic advice have not worked, the diagnosis is usually the thing that needs revisiting, not the effort.",
 "activity":"Adams Canyon, Hill AFB, and Layton youth sports",
 "activity_body":"Steep-canyon descents, occupational footwear, and adolescent growth spurts are three different mechanisms that all end in foot pain. In young athletes especially, pain at the back of the heel during a growth spurt is usually not tendonitis &mdash; it is the growth plate, and it needs a different plan than an adult heel.",
 "conditions_intro":"Layton brings us canyon injuries, military and occupational foot problems, and a heavy youth-sports load. We treat all of it:",
 "same_day":"If you come off Adams Canyon unable to put weight through the foot, that is a same-day problem rather than a wait-until-Monday problem. Call as early as you can and we will try to get you assessed and imaged the same day.",
 "insurance_note":"Tricare is widely held across Layton and the Hill AFB community, and we work with it. Military and DoD-affiliated patients should mention that when they call so we can verify coverage in advance.",
 "faqs_local":[
   ("How far is your clinic from Layton?","About twelve minutes. Take I-15 south to Exit 325 (Park Lane), or US-89 south from east Layton. The clinic is at 473 W. Bourne Circle, Suite 2 in Farmington."),
   ("Do you accept Tricare for Hill AFB families?","Yes. Tricare is one of the plans we see most often from Layton, Clearfield, and Roy. Call the office before your visit and our team will confirm your specific plan and any referral requirement."),
   ("I have to pass a fitness test but my heel hurts. What are my options?","Being told to simply rest is not workable when a test is scheduled, so we plan around it. The usual approach is to offload the painful tissue while keeping you moving &mdash; the right orthotic, a footwear change, and a graded loading programme rather than a blanket prohibition. That conversation is far more useful before a stress reaction becomes a fracture."),
 ]},
{
 "slug":"clearfield-utah","city":"Clearfield","zip":"84015","clinic":"farmington","county":"Davis County",
 "neighbors":"Layton, Syracuse, Sunset, Roy, and Hill Air Force Base",
 "drive":"about 17 minutes",
 "route":"I-15 south to Exit 325 (Park Lane). From near Clearfield Station, the FrontRunner south to Farmington Station also puts you within a few minutes of the clinic.",
 "lede":"Clearfield is roughly seventeen minutes from our Farmington clinic, and it is one of the few communities in our service area where the FrontRunner is a genuinely practical way to get to an appointment.",
 "local_1":"The Freeport Center and the Hill Air Force Base workforce define much of what we treat here. Warehouse and depot work means ten-hour days on sealed concrete in steel-toe boots, and concrete does not forgive. Plantar fasciitis, forefoot pain, and thickened or ingrown nails are the everyday consequences, and most respond well to a proper insole and a correctly sized boot long before anything surgical is on the table.",
 "local_2":"Clearfield also has a significant diabetic population, and here we would rather be blunt than polite: if you have diabetes and any numbness in your feet, you should be checking them daily and having them examined at least annually, whether or not anything hurts. Neuropathy removes the warning signal, and the wounds that matter most are the ones that never hurt at all.",
 "local_3":"The FrontRunner option genuinely changes what is possible for some Clearfield patients. Post-operative patients who cannot drive, and patients in a walking boot who would rather not manage a freeway commute, can reach Farmington Station and get to the clinic without needing someone to take a day off work. It is worth asking about when scheduling if driving is going to be difficult.",
 "activity":"Freeport Center, Hill AFB, and life on concrete",
 "activity_body":"Concrete is the common thread in Clearfield foot pain. It is unyielding, so every step returns the full load to the heel and forefoot, and safety footwear is usually stiff enough to prevent the foot from absorbing much of it. Orthotics built specifically for work boots, and a boot that actually fits, do more here than any amount of rest a shift schedule will never allow.",
 "conditions_intro":"Occupational overuse and diabetic foot care make up much of our Clearfield caseload, alongside the full range of foot and ankle conditions:",
 "same_day":"Diabetic wounds are the priority for same-day care in Clearfield. A new ulcer, a colour change, drainage, or an area of warmth should be seen within days, not weeks &mdash; early treatment is the difference between wound care and something far more serious.",
 "insurance_note":"Between Hill AFB and the Freeport Center employers, we see a lot of Tricare and PEHP from Clearfield. Both are accepted; call ahead and we will verify your plan and any referral requirement.",
 "faqs_local":[
   ("How far is your clinic from Clearfield?","About seventeen minutes by car &mdash; I-15 south to Exit 325 (Park Lane). The FrontRunner from Clearfield Station to Farmington Station is also practical, and the clinic is a short distance from the station."),
   ("I stand on concrete all day and my heels ache. Is that just normal?","Common is not the same as normal, and it is not something you have to accept. Continuous load on an unyielding surface in stiff safety footwear is one of the most reliable causes of plantar fasciitis we see. It responds well to the right insole, footwear changes, and a targeted stretching programme &mdash; and it gets harder to treat the longer it runs."),
   ("Can I be seen without taking a full day off work?","Usually. We schedule early-morning appointments and our clinic runs to time, so most routine visits take well under an hour door to door. If driving is the obstacle, the FrontRunner from Clearfield Station is a workable alternative."),
 ]},
{
 "slug":"ogden-utah","city":"Ogden","zip":"84401","clinic":"ogden","county":"Weber County",
 "neighbors":"South Ogden, Washington Terrace, Riverdale, and North Ogden",
 "drive":"about 8 minutes",
 "route":"Washington Boulevard south to Chambers Street, or I-15 south to the 5600 South exit and east. From downtown Ogden it is a short, direct drive.",
 "lede":"Our South Ogden clinic is about eight minutes from downtown Ogden, and it is built for the way this city actually moves &mdash; ski season, race season, and a river parkway that never really empties out.",
 "local_1":"Ogden is a mountain-sports town with a mountain-sports injury profile. Snowbasin, Powder Mountain, and Nordic Valley fill our winter schedule with boot-related forefoot pain, bruised toenails, and the ankle and midfoot injuries that follow a bad landing or a binding that did not release. The Ogden River Parkway and the spring race calendar fill the rest of the year with running injuries &mdash; plantar fasciitis, Achilles tendonitis, and metatarsal stress reactions.",
 "local_2":"Ski boots deserve a specific warning. A boot too tight for too long causes more than discomfort: it drives ingrown toenails, subungual haematomas, and nerve irritation across the forefoot. If your toes go numb every time you buckle in, that is not something to tolerate for an entire season &mdash; it is usually a fit problem we can help you solve before it becomes a nail you lose.",
 "local_3":"Ogden&rsquo;s student population adds a distinct pattern. Weber State students tend to arrive late, after weeks of self-treatment, often because a foot problem does not feel serious enough to justify a clinic visit between classes and shifts. Stress fractures are the ones we most wish we had seen earlier &mdash; they are straightforward when caught in the reaction stage and considerably less so once the bone has actually cracked.",
 "activity":"Snowbasin, Powder Mountain, and the Ogden River Parkway",
 "activity_body":"Ski and snowboard injuries cluster in the forefoot and the ankle; running injuries cluster in the heel and the metatarsals. Ogden generates both, often in the same patient across a single year. The useful question is rarely which sport caused it &mdash; it is which tissue is being loaded past its tolerance, and what has to change for that to stop.",
 "conditions_intro":"Winter sports injuries and running overuse dominate what Ogden brings us, alongside the full range of foot and ankle conditions:",
 "same_day":"Ski and snowboard injuries are the classic same-day case here. If you cannot bear weight after a fall, or the foot is visibly swollen and deformed, call from the mountain rather than waiting until Monday &mdash; midfoot injuries in particular do badly when they are walked on for a week.",
 "insurance_note":"We accept nearly all major carriers, and we see a lot of student and university-affiliated plans from the Weber State community. Call ahead if you are unsure whether yours is in-network.",
 "faqs_local":[
   ("How far is your clinic from downtown Ogden?","About eight minutes. Take Washington Boulevard south to Chambers Street, or I-15 south to the 5600 South exit and head east. Our South Ogden clinic is at 945 Chambers Street, Suite 3."),
   ("My toes go numb in my ski boots. Should I be worried?","It is worth sorting out rather than tolerating. Numbness usually reflects a boot that is too tight or poorly shaped for your foot, compressing the nerves across the forefoot. Left alone for a full season it can cause lasting nerve irritation, and it also drives ingrown toenails and bruised nail beds. A fit assessment and, where appropriate, a custom device usually resolves it."),
   ("I hurt my midfoot in a snowboard fall and it still hurts weeks later. What could that be?","A midfoot injury that is still painful weeks later needs imaging. <a href=\"lisfranc-injuries.html\">Lisfranc injuries</a> are frequently mistaken for a bad sprain, and they are one of the injuries where a delayed diagnosis genuinely changes the outcome. If the top of your foot is still swollen or bruised, or it hurts to push off, have it properly assessed."),
 ]},
{
 "slug":"roy-utah","city":"Roy","zip":"84067","clinic":"ogden","county":"Weber County",
 "neighbors":"Riverdale, Clearfield, Sunset, West Haven, and Hill Air Force Base",
 "drive":"about 12 minutes",
 "route":"East on 5600 South to Riverdale Road, then continue toward South Ogden and Chambers Street.",
 "lede":"Roy is about twelve minutes west of our South Ogden clinic, and with Hill Air Force Base on the doorstep a large share of the patients we see from Roy are dealing with feet that have to perform on a schedule.",
 "local_1":"Hill AFB shapes the foot problems we see in Roy more than any trail or park does. Shift work in mandated footwear, physical-fitness requirements that do not pause for an aching heel, and long stretches of standing all point the same direction: plantar fasciitis, Achilles tendonitis, and metatarsal stress reactions.",
 "local_2":"The other consistent theme in Roy is care that was postponed. Nail problems, bunions, and heel pain get tolerated for months because the schedule never quite allows for an appointment. Almost all of them are simpler, cheaper, and less invasive to treat early &mdash; an ingrown toenail dealt with in the office in twenty minutes is a very different experience from one that has been infected for six weeks.",
 "local_3":"Roy also sits on the Denver &amp; Rio Grande Western Rail Trail, which gives the city a long, flat, uninterrupted running and cycling surface. That is genuinely good for fitness and mildly bad for feet, for the same reason any flat repetitive surface is: nothing varies, so the same tissues take the same load stride after stride. High mileage there without cross-training is a common route into heel pain.",
 "activity":"Hill Air Force Base, shift work, and fitness standards",
 "activity_body":"When fitness tests are mandatory, the usual advice to simply rest is not workable. The realistic plan is to offload the painful tissue while keeping you moving &mdash; the right orthotic, a change in footwear, a targeted loading programme rather than a blanket prohibition. That is the conversation we would rather have early than after a stress reaction becomes a fracture.",
 "conditions_intro":"Military and occupational foot problems make up much of our Roy caseload, alongside the everyday conditions we treat for every patient:",
 "same_day":"If a nail has become red, hot, and painful to touch, that is an infection rather than an inconvenience, and it should be treated within a day or two. We keep same-day slots for exactly this, and the in-office procedure takes about twenty minutes.",
 "insurance_note":"Tricare is very common in Roy given the proximity to Hill AFB, and we accept it. Mention it when you call and our team will confirm your plan details and whether a referral is required.",
 "faqs_local":[
   ("How far is your clinic from Roy?","About twelve minutes. Head east on 5600 South to Riverdale Road and continue toward South Ogden. The clinic is at 945 Chambers Street, Suite 3, South Ogden."),
   ("Do you accept Tricare?","Yes. Given how many of our Roy patients are connected to Hill Air Force Base, Tricare is one of the plans we handle most often. Call ahead and we will verify your specific plan and any referral requirement before your visit."),
   ("How long does treating an ingrown toenail actually take?","The procedure itself usually takes around twenty minutes in the office under local anaesthetic, and most patients walk out and drive themselves home. Treating it early is considerably simpler than treating it after weeks of infection. See <a href=\"ingrown-nails.html\">ingrown toenail treatment</a> for what to expect."),
 ]},
{
 "slug":"riverdale-utah","city":"Riverdale","zip":"84405","clinic":"ogden","county":"Weber County",
 "neighbors":"South Ogden, Roy, Washington Terrace, and West Haven",
 "drive":"about 7 minutes",
 "route":"East on Riverdale Road toward South Ogden, then south to Chambers Street.",
 "lede":"Riverdale is roughly seven minutes from our South Ogden clinic &mdash; close enough that most patients can get an urgent foot problem seen the same day without rearranging their week.",
 "local_1":"Riverdale Road is one of the busiest retail corridors in Weber County, and retail and restaurant work is hard on feet in a way that rarely gets taken seriously until it is chronic. Eight hours of standing and pivoting on hard flooring, usually in unsupportive shoes chosen to meet a dress code, is a reliable recipe for plantar fasciitis, forefoot pain, and bunion irritation.",
 "local_2":"The Weber River Parkway runs through town and gives Riverdale a genuinely good flat running and walking surface. That is a benefit, but flat repetitive mileage has its own failure mode &mdash; the same tissues absorbing the same load every stride, which is what becomes heel pain and metatarsal stress reactions when weekly distance climbs quickly.",
 "local_3":"Retail schedules also make follow-up unusually hard, which is part of why we place weight on getting the first visit right. Where it is clinically appropriate we would rather diagnose, image, and begin treatment in a single appointment than book someone back three times &mdash; particularly for workers whose hours change week to week and who cannot easily plan around a clinic timetable.",
 "activity":"Retail shift work and the Weber River Parkway",
 "activity_body":"Standing all day and running several miles a day sound like opposites, but they injure the same structures. Both concentrate repeated load through the heel and the ball of the foot without much variation. The fix is usually a combination of better footwear, a properly built orthotic, and a graded return rather than an abrupt stop.",
 "conditions_intro":"Retail and hospitality foot problems are our most common presentation from Riverdale, but we treat the full range:",
 "same_day":"Seven minutes from the clinic means an acute problem does not need to become a chronic one. Sudden severe heel pain, an infected nail, or an injury that stops you weight-bearing should prompt a call the same day.",
 "insurance_note":"We accept nearly all major carriers. If you work retail along Riverdale Road and have recently moved onto an employer plan, call and we will check in-network status before you come in.",
 "faqs_local":[
   ("How far is your clinic from Riverdale?","About seven minutes. Take Riverdale Road east toward South Ogden and continue to Chambers Street. Our clinic is at 945 Chambers Street, Suite 3."),
   ("I stand all day at work. What shoes should I be wearing?","There is no single answer, because it depends on your foot shape and what is actually causing the pain &mdash; but the common failures are a sole that is too flexible through the midfoot, a heel counter that collapses, and a shoe that is simply too old. Bring the shoes you actually wear to your appointment; assessing them is often more useful than any general advice we could give here."),
   ("Can my heel pain be treated in one visit?","Often the diagnosis and the start of treatment can happen in a single appointment, including imaging if it is needed and an in-office injection where appropriate. Full resolution usually takes longer than one visit, but you should not have to come back three times before anything begins."),
 ]},
{
 "slug":"north-ogden-utah","city":"North Ogden","zip":"84414","clinic":"ogden","county":"Weber County",
 "neighbors":"Pleasant View, Harrisville, Ogden, and Eden",
 "drive":"about 18 minutes",
 "route":"Washington Boulevard (US-89) south through Ogden, then east to Chambers Street. Allow a little longer during the afternoon commute.",
 "lede":"North Ogden is about eighteen minutes from our South Ogden clinic, and it sends us the most consistently mountain-driven set of foot and ankle injuries in our service area.",
 "local_1":"Ben Lomond and the North Ogden Divide are the defining features here. The Ben Lomond trail is a long, sustained climb with an equally long descent, and long descents are what injure feet &mdash; Achilles tendonitis, plantar fascia strain, blackened toenails from repeated toe-box contact, and inversion ankle sprains on loose rock. The Divide adds a steady population of road cyclists dealing with forefoot numbness and pressure from stiff cleated shoes.",
 "local_2":"Because North Ogden is our furthest regular catchment, we try to make the trip count. Where it is clinically appropriate we will handle diagnosis, imaging review, and in-office treatment in a single visit rather than asking you to drive down the valley twice for something that could have been finished the first time.",
 "local_3":"Elevation and aspect also make North Ogden a genuinely seasonal referral pattern. The north-facing slopes above town hold snow and ice later than anywhere else in our service area, which pushes the spring hiking surge later and extends the winter slip-and-fall season. We see North Ogden ankle fractures from ice well after Ogden proper has dried out.",
 "activity":"Ben Lomond, the North Ogden Divide, and cycling",
 "activity_body":"Cycling foot pain is its own category and is frequently misdiagnosed. Numbness across the ball of the foot on long rides usually reflects cleat position or a shoe too narrow under load, not a nerve problem requiring surgery. It is worth getting that distinction right before anyone operates.",
 "conditions_intro":"Long-descent trail injuries and cycling-related forefoot problems are what North Ogden brings us most, alongside the full range of foot and ankle care:",
 "same_day":"Given the drive, call before you set off if the problem is acute &mdash; we will tell you honestly whether it needs same-day assessment or whether it can safely wait for a scheduled appointment. An inability to bear weight always warrants the trip.",
 "insurance_note":"We accept nearly all major carriers. Because North Ogden is our longest regular drive, we will verify your coverage over the phone before you make the trip rather than leaving it to check-in.",
 "faqs_local":[
   ("How far is your clinic from North Ogden?","About eighteen minutes. Take Washington Boulevard (US-89) south through Ogden, then head east to Chambers Street. The clinic is at 945 Chambers Street, Suite 3, South Ogden."),
   ("My feet go numb on long rides over the Divide. What causes that?","Most often cleat position, shoe width under load, or excessive shoe stiffness compressing the nerves between the metatarsals. It is usually a fitting and footwear problem rather than a surgical one, which is exactly why it is worth having assessed before anybody suggests an operation. A neuroma can produce similar symptoms and is treated differently."),
   ("Is it worth the drive, or should I find someone closer?","That is a fair question for an eighteen-minute drive, and the honest answer is that it depends on the problem. For a straightforward issue, closer is fine. For anything involving surgery, complex fracture care, or a problem that has already failed one round of treatment, seeing a foot and ankle specialist is usually worth the extra distance."),
 ]},
]

CONDITION_LINKS = """      <ul>
        <li><a href="plantar-fasciitis.html">Plantar fasciitis</a> and chronic <a href="heel-pain.html">heel pain</a></li>
        <li><a href="bunion-removal.html">Bunions</a>, including <a href="lapiplasty.html">Lapiplasty</a> 3D bunion correction</li>
        <li><a href="ingrown-nails.html">Ingrown toenails</a> and fungal nail problems</li>
        <li><a href="ankle-fractures.html">Ankle fractures</a>, sprains, and <a href="lateral-ankle-instability.html">ankle instability</a></li>
        <li><a href="achilles-tendonitis.html">Achilles tendonitis</a> and tendon injuries</li>
        <li><a href="flat-feet.html">Flat feet</a> and <a href="custom-orthotics.html">custom orthotics</a></li>
        <li><a href="diabetic-foot-care-1.html">Diabetic foot care</a> and <a href="limb-salvage.html">limb salvage</a></li>
        <li><a href="hallux-rigidus.html">Hallux rigidus</a>, <a href="gout.html">gout</a>, and <a href="arthritis.html">arthritis</a></li>
      </ul>"""


def js(s):
    return json.dumps(s, ensure_ascii=False)


def plain(s):
    """HTML fragment -> plain text for JSON-LD values."""
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", _html.unescape(s)).strip()


def build(c):
    cl = CLINICS[c["clinic"]]
    other = CLINICS["ogden" if c["clinic"] == "farmington" else "farmington"]
    city, slug = c["city"], c["slug"]
    url = f"https://www.wasatchfai.com/{slug}.html"

    title = f"{city} Podiatrist &amp; Foot Doctor | Wasatch FAI"
    desc = (f"Foot &amp; ankle care for {city}, UT. Our {cl['name']} clinic is {c['drive']} away. "
            f"Same-day appointments, most insurance accepted. Call {cl['phone']}.")

    # 3 city-specific FAQs + 2 shared. Keeping only genuinely universal answers
    # shared is what keeps pairwise uniqueness above the floor.
    faqs = list(c["faqs_local"]) + [
        ("What should I bring to my first appointment?",
         "Bring your photo ID, insurance card, a list of current medications, and any recent X-rays or "
         "records for your foot or ankle. Bringing the shoes you wear most often helps us assess your "
         "gait. You can complete our <a href=\"patient-intake-forms.html\">new-patient forms</a> in "
         "advance to save time at check-in."),
        ("What are your hours?",
         "Monday through Thursday, 8:00a to 5:00p, and Friday 8:00a to 12:00p. We are closed weekends. "
         "Same-day slots for urgent problems are released each morning, so calling early gives you the "
         "best chance of being seen that day."),
    ]

    faq_html = "\n".join(
        f"""      <details class="faq-item">
        <summary>{q}</summary>
        <div class="faq-answer">
          <p>{a}</p>
        </div>
      </details>""" for q, a in faqs)

    faq_json = ",\n".join(
        f"""        {{
          "@type": "Question",
          "name": {js(plain(q))},
          "acceptedAnswer": {{ "@type": "Answer", "text": {js(plain(a))} }}
        }}""" for q, a in faqs)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="author" content="Wasatch Foot &amp; Ankle Institute">

<!-- Open Graph -->
<meta property="og:type" content="business.business">
<meta property="og:site_name" content="Wasatch Foot &amp; Ankle Institute">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://www.wasatchfai.com/images/hero-mountain-biking.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://www.wasatchfai.com/images/hero-mountain-biking.jpg">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="css/site.css">
</head>
<body>

{TOPBAR_HEADER}

<!-- BREADCRUMB -->
<nav class="breadcrumb" aria-label="Breadcrumb">
  <div class="container">
    <ol>
      <li><a href="index.html">Home</a></li>
      <li><a href="locations.html">Locations</a></li>
      <li aria-current="page">{city}</li>
    </ol>
  </div>
</nav>

<!-- HERO -->
<section class="detail-hero" style="background-image:url('images/hero-mountain-biking.jpg')">
  <div class="container detail-hero-inner">
    <span class="visually-hidden">A mountain trail in the Wasatch range above {city}, Utah</span>
    <span class="eyebrow">Northern Utah &middot; {c['county']}</span>
    <h1>Podiatrist Serving {city}, Utah</h1>
    <p class="detail-hero-lede">{c['lede']}</p>
  </div>
</section>

<!-- NEAREST CLINIC + MAP -->
<section class="loc-section">
  <div class="container loc-layout">
    <div class="loc-card reveal">
      <h2>Your nearest clinic: {cl['name']}</h2>
      <div class="loc-card-row">
        <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8 2 5 5 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-4-3-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
        <div><strong>Address</strong><span>{cl['street']}<br>{cl['city']}, UT {cl['zip']}</span></div>
      </div>
      <div class="loc-card-row">
        <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57-.35-.11-.74-.03-1.02.24l-2.2 2.2c-2.83-1.44-5.15-3.75-6.59-6.58l2.2-2.21c.28-.27.36-.66.25-1.01-.37-1.12-.57-2.32-.57-3.57 0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1z"/></svg>
        <div><strong>Phone</strong><span><a href="tel:{cl['tel']}">{cl['phone']}</a></span></div>
      </div>
      <div class="loc-card-row">
        <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>
        <div><strong>Drive time from {city}</strong><span>{c['drive']}</span></div>
      </div>
      <div class="loc-card-row">
        <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
        <div><strong>Email</strong><span><a href="mailto:contactus@wasatchfai.com">contactus@wasatchfai.com</a></span></div>
      </div>
      <div class="hours loc-hours">
        <strong>Hours</strong>
        Mon&ndash;Thu: 8:00a &ndash; 5:00p<br>Fri: 8:00a &ndash; 12:00p<br>Sat&ndash;Sun: Closed
      </div>
      <a href="book-appointment.html" class="btn btn-primary btn-arrow loc-card-btn">Request Appointment</a>
    </div>

    <div class="loc-map-wrap reveal">
      <iframe
        src="https://www.google.com/maps?q={cl['map_q']}&amp;output=embed"
        title="Map showing Wasatch Foot &amp; Ankle Institute, {cl['street']}, {cl['city']}, UT {cl['zip']}"
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        allowfullscreen></iframe>
    </div>
  </div>
</section>

<!-- BODY -->
<section class="detail-section">
  <div class="container detail-layout">
    <article class="detail-body">
      <h2 id="foot-ankle-care">Foot &amp; ankle care for {city} and {c['county']}</h2>
      <p>{c['local_1']}</p>
      <p>{c['local_2']}</p>
      <p>{c['local_3']}</p>

      <h2 id="what-we-see">{c['activity']}</h2>
      <p>{c['activity_body']}</p>

      <h2 id="getting-here">Getting to the clinic from {city}</h2>
      <p>{c['route']} Our {cl['name']} clinic is at {cl['street']}, {cl['city']}, UT {cl['zip']}. Free surface parking sits directly outside the building, and both the entrance and the exam rooms are on ground level. We also serve {c['neighbors']} from this location.</p>

      <h2 id="same-day">Same-day appointments for {city} patients</h2>
      <p>{c['same_day']} Call <a href="tel:{cl['tel']}">{cl['phone']}</a> as early in the day as you can.</p>

      <h2 id="conditions">Conditions we treat</h2>
      <p>{c['conditions_intro']}</p>
{CONDITION_LINKS}
      <p>Browse the full <a href="services.html">list of services</a>, or read our <a href="blog.html">patient education library</a> if you would rather understand the problem before booking.</p>

      <h2 id="insurance">Insurance &amp; payment</h2>
      <p>{c['insurance_note']} We accept nearly all major carriers, including United Healthcare, Medicare, Blue Cross Blue Shield, PEHP, Tricare, and Aetna. You can also <a href="https://pay.InstaMed.com/WASATCHFOOT">pay a bill online</a>, or review our <a href="plans-pricing.html">insurance and payment information</a>.</p>

      <p class="detail-reviewed"><strong>Reviewed by the physicians at Wasatch Foot &amp; Ankle Institute.</strong> Our board-certified, fellowship-trained podiatrists care for {city} and the surrounding {c['county']} communities from clinics in <a href="farmington-utah.html">Farmington</a> and <a href="ogden-utah-foot-doctor.html">South Ogden</a>. This page is general information and is not a substitute for an in-person evaluation.</p>
    </article>

    <aside class="detail-aside">
      <div class="aside-card">
        <h3>Both of our clinics</h3>
        <p>Two locations, one team. {city} patients are closest to {cl['name']}, but you are welcome at either.</p>
        <div class="aside-phones">
          <a href="{cl['page']}" class="aside-phone">
            <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8 2 5 5 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-4-3-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
            <div><strong>{cl['name']} (nearest)</strong><span>{cl['street']}</span></div>
          </a>
          <a href="tel:{cl['tel']}" class="aside-phone">
            <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57-.35-.11-.74-.03-1.02.24l-2.2 2.2c-2.83-1.44-5.15-3.75-6.59-6.58l2.2-2.21c.28-.27.36-.66.25-1.01-.37-1.12-.57-2.32-.57-3.57 0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1z"/></svg>
            <div><strong>Call {cl['name']}</strong><span>{cl['phone']}</span></div>
          </a>
          <a href="{other['page']}" class="aside-phone">
            <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8 2 5 5 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-4-3-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
            <div><strong>{other['name']}</strong><span>{other['street']}</span></div>
          </a>
        </div>
        <a href="locations.html" class="btn btn-secondary btn-arrow aside-btn">All Locations</a>
      </div>
    </aside>
  </div>
</section>

<!-- APPOINTMENT FORM -->
<section class="contact" id="appointment">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow" style="color:#ffd6a8">Request an Appointment</span>
      <h2>{city} patients: let&rsquo;s get you on the books.</h2>
      <p>Tell us a bit about you and we&rsquo;ll be in touch within one business day. Same-day appointments are available for emergencies.</p>
    </div>
    <div class="contact-grid">
      <div class="locations reveal">
        <div class="location">
          <h3><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8 2 5 5 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-4-3-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg> {cl['name']}</h3>
          <div class="location-row"><svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8 2 5 5 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-4-3-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg><div>{cl['street']}<br>{cl['city']}, UT {cl['zip']}</div></div>
          <div class="location-row"><svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57-.35-.11-.74-.03-1.02.24l-2.2 2.2c-2.83-1.44-5.15-3.75-6.59-6.58l2.2-2.21c.28-.27.36-.66.25-1.01-.37-1.12-.57-2.32-.57-3.57 0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1z"/></svg><a href="tel:{cl['tel']}">{cl['phone']}</a></div>
          <div class="hours">
            <strong>Hours</strong>
            Mon&ndash;Thu: 8:00a &ndash; 5:00p<br>Fri: 8:00a &ndash; 12:00p<br>Sat&ndash;Sun: Closed
          </div>
        </div>
      </div>

      <form class="contact-form reveal" name="appointment-{slug}" method="POST" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="appointment-{slug}">
        <p style="display:none"><label>Don't fill this out: <input name="bot-field"></label></p>
        <h3>Request an appointment</h3>
        <p>We&rsquo;ll confirm your appointment within one business day.</p>
        <div class="form-row">
          <div class="form-group"><label>First name</label><input type="text" name="first-name" required></div>
          <div class="form-group"><label>Last name</label><input type="text" name="last-name" required></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label>Phone</label><input type="tel" name="phone" required></div>
          <div class="form-group"><label>Email</label><input type="email" name="email" required></div>
        </div>
        <div class="form-group">
          <label>What&rsquo;s going on with your feet?</label>
          <textarea name="message" placeholder="Briefly describe your symptoms or reason for visit..."></textarea>
        </div>
        <button type="submit" class="btn btn-primary btn-arrow">Send Request</button>
      </form>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="faq">
  <div class="container faq-inner">
    <div class="faq-head reveal">
      <span class="eyebrow">Common Questions</span>
      <h2>{city} podiatry FAQs</h2>
    </div>
    <div class="faq-list">
{faq_html}
    </div>
  </div>
</section>

<!-- CTA BAND -->
<section class="cta-band">
  <div class="container cta-band-inner reveal">
    <div>
      <span class="eyebrow" style="color:#ffe5cc">Ready When You Are</span>
      <h2>Let&rsquo;s get you back on your feet &mdash; pain-free.</h2>
      <p>Same-day appointments are available for emergencies. Reach out to our {cl['name']} team today.</p>
    </div>
    <div class="cta-band-actions">
      <a href="book-appointment.html" class="btn btn-light btn-arrow">Request Appointment</a>
      <a href="tel:{cl['tel']}" class="btn btn-ghost cta-ghost">Call {cl['name']}</a>
    </div>
  </div>
</section>

{FOOTER}

<!-- JSON-LD STRUCTURED DATA -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "@id": "{url}#breadcrumb",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.wasatchfai.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Locations", "item": "https://www.wasatchfai.com/locations.html" }},
        {{ "@type": "ListItem", "position": 3, "name": {js(city)}, "item": "{url}" }}
      ]
    }},
    {{
      "@type": "FAQPage",
      "@id": "{url}#faq",
      "mainEntity": [
{faq_json}
      ]
    }},
    {{
      "@type": "MedicalWebPage",
      "@id": "{url}#webpage",
      "url": "{url}",
      "name": {js(plain(title))},
      "description": {js(plain(desc))},
      "inLanguage": "en-US",
      "isPartOf": {{ "@id": "https://www.wasatchfai.com/#website" }},
      "about": {{ "@id": "{url}#clinic" }},
      "reviewedBy": {{ "@id": "https://www.wasatchfai.com/#clinic" }},
      "specialty": "Podiatric"
    }},
    {{
      "@type": "MedicalClinic",
      "@id": "{url}#clinic",
      "name": "Wasatch Foot & Ankle Institute — {cl['name']}",
      "url": "https://www.wasatchfai.com/{cl['page']}",
      "logo": "https://www.wasatchfai.com/images/logo-full.png",
      "image": "https://www.wasatchfai.com/images/logo-full.png",
      "telephone": "{cl['e164']}",
      "email": "contactus@wasatchfai.com",
      "medicalSpecialty": "Podiatric",
      "priceRange": "$$",
      "parentOrganization": {{ "@id": "https://www.wasatchfai.com/#clinic" }},
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "{cl['street']}",
        "addressLocality": "{cl['city']}",
        "addressRegion": "UT",
        "postalCode": "{cl['zip']}",
        "addressCountry": "US"
      }},
      "geo": {{ "@type": "GeoCoordinates", "latitude": {cl['lat']}, "longitude": {cl['lon']} }},
      "hasMap": "https://www.google.com/maps?q={cl['map_q']}",
      "areaServed": [
        {{ "@type": "City", "name": "{city}, Utah" }},
        {{ "@type": "AdministrativeArea", "name": "{c['county']}, Utah" }}
      ],
      "openingHoursSpecification": [
        {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"], "opens": "08:00", "closes": "17:00" }},
        {{ "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "12:00" }}
      ]
    }}
  ]
}}
</script>

<script src="js/site.js" defer></script>

{CALLBAR}
</body>
</html>
"""


# ------------------------------------------------------------ uniqueness ----
def content_text(page_html):
    s = re.sub(r"(?is)<(script|style|nav|header|footer|svg|form)[^>]*>.*?</\1>", " ", page_html)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", _html.unescape(s)).strip()


def shingles(t, n=8):
    w = t.lower().split()
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n))}


if __name__ == "__main__":
    pages = {c["slug"]: build(c) for c in CITIES}
    bodies = {k: content_text(v) for k, v in pages.items()}
    shs = {k: shingles(v) for k, v in bodies.items()}

    worst = sorted(
        (1 - len(shs[a] & shs[b]) / len(shs[a]), a, b)
        for a, b in itertools.permutations(shs, 2)
    )
    lo = worst[0][0]
    mean = statistics.mean(u for u, _, _ in worst)

    print("word counts (content region only):")
    for c in CITIES:
        print(f"   {len(bodies[c['slug']].split()):5d}  {c['slug']}")
    print(f"\n   median {statistics.median(len(b.split()) for b in bodies.values()):.0f} words")
    print(f"\nuniqueness: mean {mean:.1%}, minimum {lo:.1%} (floor {UNIQUENESS_FLOOR:.0%})")
    for u, a, b in worst[:3]:
        print(f"   lowest: {u:.1%}  {a} vs {b}")

    if lo < UNIQUENESS_FLOOR:
        print(f"\nFAIL: minimum uniqueness {lo:.1%} is below the {UNIQUENESS_FLOOR:.0%} floor.")
        print("Add more city-specific material before shipping these pages.")
        sys.exit(1)

    for c in CITIES:
        (ROOT / f"{c['slug']}.html").write_text(pages[c["slug"]], encoding="utf-8")
        print(f"wrote {c['slug']}.html")
    print(f"\n{len(CITIES)} city pages generated, all above the uniqueness floor.")
