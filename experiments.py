from mstudio.subs import *
import textwrap

text = """In the heart of a quaint little town nestled amidst rolling hills and whispering woods, a magical bookshop stood. Its shelves were adorned with ancient tomes, their pages imbued with secrets of forgotten lands. The shop's enigmatic owner, a wizened figure known as Mr. Alistair, possessed an uncanny ability to match readers with their perfect book. Visitors would leave with hearts enchanted, carrying tales of otherworldly adventures in their souls.

The bookstore's allure transcended generations, drawing curious souls seeking solace or thrill. No two visits were ever the same, as the shop itself seemed to rearrange its interior at will. Dusty beams of sunlight danced through crevices, illuminating rows of leather-bound wonders. Those who entered would often lose track of time, captivated by the timeless whispers of literature.

Among the bookshelves, a hidden alcove beckoned those with an explorer's spirit. Rumors spoke of a passage to a parallel realm, where fiction mingled with reality. Only the chosen one, pure of heart, could unlock the portal. Many tried, but none succeeded. Some believed the portal to be a mere metaphor for the transformative power of stories, yet others clung to the hope of transcending reality.

Once a year, on the eve of the winter solstice, the bookstore hosted a grand celebration. Book lovers and characters from tales beyond flocked to the enchanted gathering. Mr. Alistair himself would emerge from the shadows, donning a cloak of stars, ready to weave a new narrative into the collective consciousness.

In the flickering candlelight, visitors exchanged tales of their journeys, their hearts connected through shared emotions. In that magical realm of ink and imagination, the barriers between fiction and reality blurred, and every soul became a storyteller. As the clock struck midnight, the festivities dissolved, leaving everyone with a lasting gift—a deeper understanding of the threads that bound their lives to the stories they cherished. And so, the bookshop's legend continued to grow, luring dreamers and wanderers to its ever-open door.
"""

# sub_rip.save("/tmp/su.srt", encoding="utf-8")

paragraphs = text.split("\n\n")
paragraphs = ["\n".join(textwrap.wrap(p, width=50)) for p in paragraphs]
sub_rip = srt_from_paragraphs(paragraphs)


hardsub(paragraphs).write_videofile("subs.mp4", fps=24, codec="libx264")
