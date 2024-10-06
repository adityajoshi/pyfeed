import feedparser
import requests
import os
import csv
from datetime import datetime
from io import BytesIO

FEED_FOLDER = 'feeds'

RSS_FEEDS = {
    'Accidentally_in_Code': 'https://cate.blog/feed/',
    'Amit_Sengupta': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCYCVm1aN33HYdLs66DHw_ow',
    'Andreas_Kretz': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCY8mzqqGwl5_bTpBY9qLMAA',
    'baak6': 'https://baak6.com/rss.xml',
    'benkuhn': 'https://www.benkuhn.net/index.xml',
    'Aditya_Joshi': 'https://adityajoshi.github.io/index.xml',
    'Bear_Blog_Trending_Posts': 'https://bearblog.dev/discover/feed/',
    'LOW_TECH_MAGAZINE': 'https://solar.lowtechmagazine.com/feeds/all-en.atom.xml',
    'rsapkf': 'https://rsapkf.org/weblog/rss.xml',
    'The Crow': 'https://thecrow.uk/feed.xml',
    'The New Oil': 'https://write.as/thenewoil/feed/',
    'Rodrigo Ghedin': 'https://notes.ghed.in/feed.xml',
    'Tumfatig': 'https://www.tumfatig.net/index.xml',
    'BrainBaking': 'https://brainbaking.com/index.xml',
    'OpenBSD Webzine': 'https://webzine.puffy.cafe/atom.xml',
    'RoboNuggie on Odysee': 'https://odysee.com/$/rss/@RoboNuggie:0',
    'Root BSD on Odysee': 'https://odysee.com/$/rss/@rootbsd:6',
    'That grumpy BSD guy': 'https://www.blogger.com/feeds/8616610987649128333/posts/default',
    'The OpenBSD guy on Odysee': 'https://odysee.com/$/rss/@TheOpenBSDGuy:e',
    'unixsheikh.com': 'https://unixsheikh.com/feed.rss',
    'Vermaden posts': 'https://vermaden.wordpress.com/feed/',
    'Causal Agency': 'https://text.causal.agency/feed.atom',
    'The Indian Cyclist': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCXTSHJc5NgbenERc-Ku8h0Q',
    'Dennis Ivy': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCTZRcDjjkVajGL6wd76UnGg',
    'Derek Banas': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCwRXb5dUK4cvsHbx-rGzSgw',
    'Derek Kedziora': 'https://derekkedziora.com/feed.xml',
    'DW Planet A': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCb72Gn5LXaLEcsOuPKGfQOg',
    'ENDEVR': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCuw0GgMlZlAsWvpI8PgCN8g',
    'Eric Radman : A Journal': 'http://eradman.com/atom.xml',
    'freeCodeCamp.org': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC8butISFwT-Wl7EV0hUK0BQ',
    'freeCodeCamp Talks': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCVk8weS4S2kJfja72fTxh5A',
    'FreeFinacal': 'https://feeds.feedburner.com/freefincal/XFaU',
    'HNRSS - 150 points': 'https://hnrss.org/newest?points=150',
    'HNRSS - Best': 'https://hnrss.org/best',
    'HNRSS - Ask': 'https://hnrss.org/ask',
    'HNRSS - Show': 'https://hnrss.org/show',
    'HNRSS - Polls': 'https://hnrss.org/polls',
    'THAT Jeff Smith': 'https://www.thatjeffsmith.com/feed/',
    'Jakob Jenkov': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCkiRZdcuNF7aiT4sQ9MJt-Q',
    'Code with Josh': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCTWCL-kx6uUHX4g6Us9HMng',
    'Continuous Delivery': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCCfqyGl3nq_V0bo64CjZh8g',
    'Jeff Smith': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCdzrhKSHU3Tf8QDOuM7EF9g',
    'José Paumard': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCfTi77-bFEbneIBean2LnMA',
    'Julian Dontcheff Database Blog': 'https://juliandontcheff.wordpress.com/feed/',
    'Kode Vicious': 'https://queue.acm.org/rss/feeds/kodevicious.xml',
    'Lane Blog': 'https://wagslane.dev/index.xml',
    'gotbletu': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCkf4VIqu3Acnfzuk3kRIFwA',
    'Linux Journal': 'https://www.linuxjournal.com/news/feed',
    'Luke Smith': 'https://lukesmith.xyz/rss.xml',
    'Luke Smith on Odysee': 'https://odysee.com/$/rss/@Luke:7',
    'Marco Codes': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCf4tsZfSZlBx2QusJg3HJew',
    'Matt Steele': 'https://steele.blue/feed/atom.xml',
    'Midnight Pub': 'https://midnight.pub/feed.xml',
    'Nicholas Weaver': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC6tTeyrPeR5XLlVGglZowuw',
    'Philip Starritt': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC5PoZQhjD8UWude0ewKEAFA',
    'Pranjal Kamra': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCwAdQUuPT6laN-AQR17fe1g',
    'Richard Chesterwood': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCR5fgyj9JaFvTMBUrKRdqYg',
    'Rob Weychert': 'http://feeds.feedburner.com/robweychert',
    'Rubenerd': 'https://rubenerd.com/feed/',
    'Simple Programming': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCDnZ8f2yo-JGBh8rOn30OAg',
     'Solene': 'https://dataswamp.org/~solene/rss.xml',
     'Siva Academy': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCBt6VrxAIb5jLh9HLDcdwtQ',
     'The Magic of SQL': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCWeOtlakw8g01MrR8U4yYtg',
     'Standard Ebooks - Newest Ebooks': 'https://standardebooks.org/feeds/rss/new-releases',
     'Tech Coach': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCaBNj5bfIpRGuEx3k3ekNoA',
     'The jolly Teapot': 'https://thejollyteapot.com/feed.rss',
     'The Plain Text Project': 'https://plaintextproject.online',
     'Veritasium': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCHnyfMqiRRG1u-2MsSQLbXA',
     'TED-Ed': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCsooa4yRKGN_zEE8iknghZA',
     'lon_tv_blog': 'https://blog.lon.tv/feed/',
     'lon_tv_links': 'https://links.lon.tv/feed/atom?',
     'antirez.com': 'http://antirez.com/rss',
     'conners_blog': 'https://cedwards.xyz/index.xml',
     'Andrej Karpathy': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCXUPKJO5MZQN11PqgIvyuvQ',
     'Australian Settlement': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCSVQEIk_7gkKYW_WZawJicA',
     'Best Audiobooks ': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCJ5CsM8LCoqGAVn1KjZDgxQ',
     'Bike Commuter Hero': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCqlLa8Nd58M6As2ppCT_Phw',
     'CloudTrainingOCI': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC0WCUAvT1gLas0eplWJNzeQ',
     'Craft Software with Victor Rentea': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC_RV_tw0mK1aStb6h1eX77g',
     'Desmo': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCjVc08ugGY4t7qnUfTIILQw',
     'Easy Fingerstyle Tabs': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCTh2ZC2ynP6Va8edeAhRBNA',
     'Easy Guitar Tube': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCTIYCU2R74Uqz4hUTAJekIQ',
     'EuroVelo': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCiy-6K3hz8mwbzRlwsatzZA',
     'itversity': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCakdSIPsJqiOLqylgoYmwQg',
     'JitterTed': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCx8qMdZ6JoZgOcOQxWlyV8A',
     'KoreKara': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCWpmB5LNI-5LqhOZNTy8i5w',
     'Living Big In A Tiny House': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCoNTMWgGuXtGPLv9UeJZwBw',
     'Marco Codes': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCf4tsZfSZlBx2QusJg3HJew',
     'One Code Man': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC5Fmb-rqhoZwmfIBoXv6P1w',
     'Oracle Developers': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCdDhYMT2USoLdh4SZIsu_1g',
     'Oracle Learning': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCpcndhe5IebWrJrdLRGRsvw',
     'QuickRead': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCYcJwJXNsBWy5QMU74wf9UQ',
     'Reginald Scot': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCSD3vxaGGnUj39bEY2nWlkw',
     'Rerouting...': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCDw93dTtyidxczSYVg7oVjw',
     'Shifter': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC9-ZlLTioqMZowRLZHscozw',
     'SQL and Database explained!': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCVN7PnJnuKQ65QLmWjFvhiw',
     'Tech Tejendra': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCLPjhN0CNm1gUD3UoWSue1g',
     'DatabaseStar': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCIfqbXQK-Vm3V185YypcMcg',
     'IdeaSpot': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC-jn4QgSxr77aUEX9RX1jbA',
     'A_Day_In_The_Life_Of': 'https://adayinthelifeof.nl/feed/index.xml',
     'jhooq': 'https://jhooq.com/index.xml',
     'techrights.org': 'https://portal.mozz.us/gemini/gemini.techrights.org/feed.xml',
     'Field of Relax': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCtWbfjkmw1UsrZ6r67TXvFQ',
     'Find a Job in Germany': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCx5rpKOgJ709qisEXAaSbnQ',
     'Fingerstyle Club': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC2iy7HYmLymYeYEtTLKk2kA',
     'Fingerstyle Guitar Tabs': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCxnwOAkChnoTeMOM5lQbfcA',
     'JitterTed': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCx8qMdZ6JoZgOcOQxWlyV8A',
     'Marco Codes': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCf4tsZfSZlBx2QusJg3HJew',
     'Mr. Tabs': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC_cm0YPagB8p2nXd8Z8Y_TA',
     'NetworkChuck': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC9x0AN7BWHpCDHSm9NiJFJQ',
     'Notes & Beats GUITAR TABS': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCIdcLzjFL9Ct7xmFzuywO8Q',
     'Oracle Developers': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCdDhYMT2USoLdh4SZIsu_1g',
     'OSCAR India': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCwmYnS8L5mWVTCq4sPA8qWg',
     'Rahul Wagh': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC7p4oXcPbgk_yTSHK7QlkSg',
     'Reginald Scot': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCSD3vxaGGnUj39bEY2nWlkw',
     'Ryan Van Duzer': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCVcUzl95VwxrIEQnu9xI21g',
     'Shifter': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC9-ZlLTioqMZowRLZHscozw',
     'Signals Music Studio': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCRDDHLvQb8HjE2r7_ZuNtWA',
     'southeastlinuxfest': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCR3wE5C6zGVWsbdO2qEqONQ',
     'SQL and Database explained!': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCVN7PnJnuKQ65QLmWjFvhiw',
     'SSGEOS': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCvdaBhuwHK7Js106yKAe3YA',
     'The Great British Radio Play': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCHjxkbFpcNqW2eRMQmkP4xA',
     'The Magic of SQL': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCWeOtlakw8g01MrR8U4yYtg',
     'Veritasium': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCHnyfMqiRRG1u-2MsSQLbXA',
     'Yoni Schlesinger': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCmDOwRLQVMhYaGuZkDgNfUA',
     'Joseph Chloe': 'https://josephchoe.com/feed.xml',
     'sebastiano tronto': 'https://sebastiano.tronto.net/blog/feed.xml',
     'Oracle BASE': 'https://feeds.feedburner.com/TheOracleBaseBlog',
     'Dubroy': 'https://dubroy.com/blog/rss.xml',
     'Zain Rizvi': 'https://www.zainrizvi.io/rss/',
     'NeetCode': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCevUmOfLTUX9MNGJQKsPdIA',
     '512KB Club': 'https://512kb.club/feed.xml',
     'text.casual': 'https://text.causal.agency/feed.atom',
     'Pursuit of Simplicity': 'https://pursuit-of-simplicity.pages.dev/atom.xml',
     'SmarterEveryDay': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC6107grRI4m0o2-emgoDnAA',
     'spring.io_blog': 'https://spring.io/blog.atom',
     'spring developers': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC7yfnfvEUlXUIfm8rGLwZdA',
     'Coffee_Software_with_Josh_Long': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCjcceQmjS4DKBW_J_1UANow',
     'Dan_Vega': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCc98QQw1D-y38wg6mO3w4MQ',
     'DaShaun': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCuGoHRQbVXa4LxepmPOdUfQ',
     'EmbarkX': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCH_Wi8MidUKGlQvep9T7t4g',
     'Devtiro': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCSMkAXZB0IMmC-7eTUIae-w',
     'scaglio': 'https://scaglio.bearblog.dev/feed/?type=rss',
     'hanki.dev': 'https://hanki.dev/feed/',
     'Mikhal_Sapka': 'https://michal.sapka.me/index.xml',
     'bt': 'https://btxx.org/index.rss',
     'Jason_Fried': 'https://world.hey.com/jason/feed.atom',
     'Nithin_Kamath': 'https://nithinkamath.me/index.xml',
     'Steven_Lambert': 'https://stevenklambert.com/feed.xml',
     'commandlinefu': 'http://feeds2.feedburner.com/Command-line-fu',
     'Rob_knight': 'https://rknight.me/subscribe/everything/rss.xml',
     'akashgoswami.com': 'https://akashgoswami.com/articles/index.xml',
     'akashgoswami.dev': 'https://akashgoswami.dev/posts/index.xml',
     'Every_Paisa_Matters': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCE43WLnnJlOaC45v3ZFPEDQ',
     'Real_python_podcast': 'https://realpython.com/podcasts/rpp/feed',
     'Real_python_youtube': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCI0vQvr9aFn27yR6Ej6n5UA'
}


def update():
    """

    :rtype: list
    """
    articles = []
    for source, feed in RSS_FEEDS.items():
        cur_timestamp = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
        try:
            resp = requests.get(feed, timeout=20.0)
        except requests.ReadTimeout:
            print(f'Timeout when reading RSS {feed}'.ljust(50, " "), "OK")
            continue

        content = BytesIO(resp.content)
        #parsed_feed = feedparser.parse(feed)
        parsed_feed = feedparser.parse(content)
        new_entries = [
            ("False", entry.get('published', cur_timestamp), entry.get('author', 'unknown'), entry.title, entry.link)
            for entry in parsed_feed.entries]
        source = source.replace(" ","_")
        source = source.replace("-","_")
        csv_file = source + '_records'
        # write_records_to_csv(entries, source + '_records.csv')

        # Load existing records from the CSV
        existing_records = load_existing_records(csv_file)

        # Filter out entries that are already present in the CSV (based on the unique 'link' field)
        unique_entries = [entry for entry in new_entries if entry[3] not in existing_records]

        # Write only unique entries to the CSV file
        if unique_entries:
            write_records_to_csv(unique_entries, csv_file)

        print(f"{source}        OK".rjust(10," "))


def load_existing_records(csv_file):
    """
    Load existing records from the CSV file and return a set of unique links.
    :rtype: set
    """
    if not os.path.exists('feeds/' + csv_file):
        return set()  # Return empty set if file doesn't exist yet

    existing_links = set()
    with open('feeds/' + csv_file, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            if row:  # Ensure row is not empty
                existing_links.add(row[3])  # The link is at index 3 in the tuple
    return existing_links


def write_records_to_csv(records, csv_file):
    with open(os.path.join(FEED_FOLDER, csv_file), 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=",")
        # csv_writer.writerow(['id', 'win'])  # Write header

        for record in records:
            csv_writer.writerow(record)


if __name__ == "__main__":
    update()
