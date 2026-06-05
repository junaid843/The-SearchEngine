"""Generate 5 rich sample PDFs for the Mini Search Engine demo."""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

OUTPUT_DIR = "sample_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

def heading(text, level=1):
    size = {1: 20, 2: 15, 3: 12}[level]
    return Paragraph(
        f"<b>{text}</b>",
        ParagraphStyle(
            "H",
            parent=styles["Normal"],
            fontSize=size,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.HexColor("#1a237e"),
        ),
    )

def body(text):
    return Paragraph(
        text,
        ParagraphStyle(
            "B",
            parent=styles["Normal"],
            fontSize=11,
            leading=16,
            spaceAfter=8,
        ),
    )

def hr():
    return HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=10)

# ── PDF 1 – Artificial Intelligence ──────────────────────────────────────────
def pdf_ai():
    doc   = SimpleDocTemplate(f"{OUTPUT_DIR}/01_Artificial_Intelligence.pdf", pagesize=letter)
    story = []
    story.append(heading("Artificial Intelligence: An Overview"))
    story.append(hr())
    story.append(body(
        "Artificial intelligence (AI) refers to the simulation of human intelligence in machines "
        "that are programmed to think and learn. The term was coined by John McCarthy in 1956 "
        "at the Dartmouth Conference, which is widely considered the birth of AI as a field."
    ))
    story.append(heading("1. Machine Learning", 2))
    story.append(body(
        "Machine learning (ML) is a subset of AI that enables systems to learn from data without "
        "being explicitly programmed. Algorithms identify patterns, make decisions, and improve "
        "their performance with experience. Supervised learning, unsupervised learning, and "
        "reinforcement learning are the three main paradigms."
    ))
    story.append(body(
        "Deep learning uses multi-layered neural networks to model complex patterns. Convolutional "
        "neural networks (CNNs) excel at image recognition, while recurrent networks (RNNs) handle "
        "sequential data such as text and speech."
    ))
    story.append(heading("2. Natural Language Processing", 2))
    story.append(body(
        "NLP enables computers to understand, interpret, and generate human language. Applications "
        "include chatbots, sentiment analysis, machine translation, and text summarisation. "
        "Transformer-based models like BERT and GPT have revolutionised the field since 2017."
    ))
    story.append(body(
        "Large language models (LLMs) are trained on massive text corpora and can perform a wide "
        "variety of language tasks with minimal fine-tuning, a property known as few-shot learning."
    ))
    story.append(heading("3. Computer Vision", 2))
    story.append(body(
        "Computer vision allows machines to interpret visual information from the world. Use cases "
        "include autonomous driving, medical image analysis, facial recognition, and quality control "
        "in manufacturing. Object detection frameworks such as YOLO and Faster R-CNN achieve near-"
        "human accuracy on benchmark datasets."
    ))
    story.append(heading("4. Ethics in AI", 2))
    story.append(body(
        "As AI becomes more prevalent, ethical considerations grow in importance. Key issues include "
        "algorithmic bias, data privacy, transparency, and accountability. Regulatory bodies around "
        "the world are developing frameworks to ensure AI is developed and deployed responsibly."
    ))
    story.append(heading("5. Future of AI", 2))
    story.append(body(
        "Research frontiers include artificial general intelligence (AGI), which would match human "
        "cognitive ability across any domain. Neuro-symbolic AI aims to combine the pattern-"
        "recognition strength of neural networks with the reasoning power of classical AI. "
        "Quantum computing may accelerate training of future AI models."
    ))
    doc.build(story)
    print("Created 01_Artificial_Intelligence.pdf")


# ── PDF 2 – Climate Change ────────────────────────────────────────────────────
def pdf_climate():
    doc   = SimpleDocTemplate(f"{OUTPUT_DIR}/02_Climate_Change.pdf", pagesize=letter)
    story = []
    story.append(heading("Climate Change: Causes, Effects, and Solutions"))
    story.append(hr())
    story.append(body(
        "Climate change refers to long-term shifts in global temperatures and weather patterns. "
        "While natural factors play a role, scientific consensus confirms that human activities "
        "have been the dominant driver of climate change since the mid-20th century."
    ))
    story.append(heading("1. Greenhouse Gas Emissions", 2))
    story.append(body(
        "The burning of fossil fuels—coal, oil, and natural gas—releases carbon dioxide (CO2) "
        "and methane (CH4) into the atmosphere. These greenhouse gases trap heat, raising the "
        "Earth's average temperature. CO2 concentrations have risen from 280 ppm before "
        "industrialisation to over 420 ppm today."
    ))
    story.append(heading("2. Observed Impacts", 2))
    story.append(body(
        "Consequences of rising temperatures include: rising sea levels due to glacial melt, "
        "more frequent and intense extreme weather events (hurricanes, droughts, heatwaves), "
        "ocean acidification harming marine ecosystems, and shifts in biodiversity as species "
        "migrate toward cooler habitats."
    ))
    story.append(heading("3. The Paris Agreement", 2))
    story.append(body(
        "Adopted in 2015, the Paris Agreement commits nations to limit global warming to well "
        "below 2 degrees Celsius above pre-industrial levels, with efforts to stay below 1.5 C. "
        "Countries submit Nationally Determined Contributions (NDCs) outlining their climate "
        "action plans, which are updated every five years."
    ))
    story.append(heading("4. Renewable Energy Transition", 2))
    story.append(body(
        "Solar and wind power have seen dramatic cost reductions—solar photovoltaic costs dropped "
        "by nearly 90 percent in the decade to 2023. Electric vehicles, green hydrogen, and "
        "energy storage technologies are also critical components of the low-carbon transition."
    ))
    story.append(heading("5. Carbon Capture and Removal", 2))
    story.append(body(
        "Beyond emissions reductions, negative-emission technologies such as direct air capture "
        "(DAC), bioenergy with carbon capture and storage (BECCS), and natural solutions like "
        "reforestation and wetland restoration are considered necessary to meet climate targets."
    ))
    doc.build(story)
    print("Created 02_Climate_Change.pdf")


# ── PDF 3 – Space Exploration ─────────────────────────────────────────────────
def pdf_space():
    doc   = SimpleDocTemplate(f"{OUTPUT_DIR}/03_Space_Exploration.pdf", pagesize=letter)
    story = []
    story.append(heading("Space Exploration: Past, Present, and Future"))
    story.append(hr())
    story.append(body(
        "Space exploration has captivated humanity since the launch of Sputnik 1 by the Soviet "
        "Union on 4 October 1957, marking the beginning of the Space Age. Since then, humans "
        "have landed on the Moon, deployed robotic probes to every planet in the solar system, "
        "and established a continuous human presence in low Earth orbit."
    ))
    story.append(heading("1. The Space Race", 2))
    story.append(body(
        "The Cold War rivalry between the United States and the Soviet Union drove rapid "
        "advances in rocket technology. Key milestones include Yuri Gagarin's orbital flight "
        "(1961), the first spacewalk by Alexei Leonov (1965), and NASA's Apollo 11 mission that "
        "put Neil Armstrong and Buzz Aldrin on the Moon in July 1969."
    ))
    story.append(heading("2. The International Space Station", 2))
    story.append(body(
        "The ISS is a collaborative project involving NASA, Roscosmos, ESA, JAXA, and CSA. "
        "It has been continuously inhabited since November 2000 and serves as a microgravity "
        "laboratory for research in biology, physics, astronomy, and medicine."
    ))
    story.append(heading("3. Mars Exploration", 2))
    story.append(body(
        "NASA's Perseverance rover, which landed in Jezero Crater in February 2021, is searching "
        "for signs of ancient microbial life and collecting rock samples for future return to Earth. "
        "China's Tianwen-1 mission also successfully deployed the Zhurong rover in May 2021."
    ))
    story.append(heading("4. Artemis and Lunar Return", 2))
    story.append(body(
        "NASA's Artemis programme aims to return humans to the Moon, including the first woman "
        "and first person of colour, using the Space Launch System (SLS) and the Orion capsule. "
        "The Lunar Gateway, a small space station in lunar orbit, will support long-duration "
        "surface missions and serve as a staging point for Mars."
    ))
    story.append(heading("5. Commercial Spaceflight", 2))
    story.append(body(
        "Companies such as SpaceX, Blue Origin, and Rocket Lab have transformed the economics "
        "of launch. SpaceX's reusable Falcon 9 has dramatically cut costs, and Starship—the "
        "largest rocket ever built—is intended to carry humans to Mars. Commercial crew "
        "programmes have ended US dependence on Russian Soyuz for ISS transport."
    ))
    doc.build(story)
    print("Created 03_Space_Exploration.pdf")


# ── PDF 4 – Cybersecurity ─────────────────────────────────────────────────────
def pdf_cyber():
    doc   = SimpleDocTemplate(f"{OUTPUT_DIR}/04_Cybersecurity.pdf", pagesize=letter)
    story = []
    story.append(heading("Cybersecurity: Protecting the Digital World"))
    story.append(hr())
    story.append(body(
        "Cybersecurity is the practice of protecting systems, networks, and programs from digital "
        "attacks. These cyberattacks typically aim to access, change, or destroy sensitive "
        "information, extort money, or disrupt normal business processes."
    ))
    story.append(heading("1. Common Threat Vectors", 2))
    story.append(body(
        "Phishing attacks trick users into revealing credentials or installing malware via "
        "deceptive emails or websites. Ransomware encrypts victim data and demands payment "
        "for decryption keys. SQL injection exploits database vulnerabilities. Zero-day "
        "vulnerabilities are flaws unknown to the vendor and exploited before patches exist."
    ))
    story.append(heading("2. Encryption and PKI", 2))
    story.append(body(
        "Encryption converts readable data into ciphertext. Symmetric encryption (AES) uses "
        "one key; asymmetric encryption (RSA, ECC) uses a public/private key pair. TLS/SSL "
        "secures data in transit on the web. Public Key Infrastructure (PKI) manages digital "
        "certificates that bind public keys to identities."
    ))
    story.append(heading("3. Zero Trust Architecture", 2))
    story.append(body(
        "Zero Trust is a security model that assumes no user or device is inherently trusted, "
        "inside or outside the network perimeter. It requires continuous verification, least-"
        "privilege access, and micro-segmentation. Organisations adopting Zero Trust saw a "
        "significant reduction in breach costs according to IBM's 2023 Cost of a Data Breach report."
    ))
    story.append(heading("4. Incident Response", 2))
    story.append(body(
        "A structured incident response plan includes: preparation, identification, containment, "
        "eradication, recovery, and lessons learned (PICERL). Security Operations Centers (SOCs) "
        "use SIEM tools to aggregate logs and detect anomalies in real time."
    ))
    story.append(heading("5. Regulatory Landscape", 2))
    story.append(body(
        "Regulations such as GDPR (EU), CCPA (California), HIPAA (healthcare, US), and PCI-DSS "
        "(payment cards) impose data protection obligations on organisations. Non-compliance "
        "can result in substantial fines. The SEC now requires public companies to disclose "
        "material cybersecurity incidents within four business days."
    ))
    doc.build(story)
    print("Created 04_Cybersecurity.pdf")


# ── PDF 5 – Blockchain ────────────────────────────────────────────────────────
def pdf_blockchain():
    doc   = SimpleDocTemplate(f"{OUTPUT_DIR}/05_Blockchain_Technology.pdf", pagesize=letter)
    story = []
    story.append(heading("Blockchain Technology: Principles and Applications"))
    story.append(hr())
    story.append(body(
        "A blockchain is a distributed ledger that records transactions across many computers "
        "so that the record cannot be altered retroactively without alteration of all subsequent "
        "blocks and the consensus of the network. Bitcoin, introduced in 2009 by the pseudonymous "
        "Satoshi Nakamoto, was the first practical implementation."
    ))
    story.append(heading("1. Core Concepts", 2))
    story.append(body(
        "Each block contains a cryptographic hash of the previous block, a timestamp, and "
        "transaction data. The chain is immutable: changing one block invalidates every "
        "subsequent block. Consensus mechanisms—Proof of Work (PoW) and Proof of Stake (PoS)—"
        "ensure agreement among distributed nodes without a central authority."
    ))
    story.append(heading("2. Smart Contracts", 2))
    story.append(body(
        "Smart contracts are self-executing programs stored on a blockchain that automatically "
        "enforce the terms of an agreement when predefined conditions are met. Ethereum, launched "
        "in 2015, popularised smart contracts and underpins most DeFi (decentralised finance) "
        "and NFT (non-fungible token) applications."
    ))
    story.append(heading("3. Decentralised Finance (DeFi)", 2))
    story.append(body(
        "DeFi replicates traditional financial services—lending, borrowing, trading—using smart "
        "contracts, eliminating intermediaries such as banks. Automated market makers (AMMs) like "
        "Uniswap allow token swaps without order books. Total value locked (TVL) in DeFi protocols "
        "peaked at over 180 billion USD in late 2021."
    ))
    story.append(heading("4. Enterprise Blockchain", 2))
    story.append(body(
        "Permissioned blockchains such as Hyperledger Fabric and R3 Corda are used in supply "
        "chain management, trade finance, and healthcare to improve transparency and reduce "
        "reconciliation costs. IBM Food Trust uses Hyperledger to trace produce from farm to shelf."
    ))
    story.append(heading("5. Challenges and Outlook", 2))
    story.append(body(
        "Scalability (the blockchain trilemma), energy consumption (PoW), regulatory uncertainty, "
        "and user experience remain key challenges. Layer-2 solutions like the Lightning Network "
        "and Ethereum rollups address throughput. Central bank digital currencies (CBDCs) are "
        "being explored by over 100 countries as government-backed digital money."
    ))
    doc.build(story)
    print("Created 05_Blockchain_Technology.pdf")


if __name__ == "__main__":
    pdf_ai()
    pdf_climate()
    pdf_space()
    pdf_cyber()
    pdf_blockchain()
    print("\nAll 5 sample PDFs created successfully in ./sample_pdfs/")
