import pandas as pd
import random

# Malaysian-specific scam triggers
SCAM_PHRASES = [
    "This is from Bank Negara Malaysia, your credit card account is compromised.",
    "Urgent: Your Maybank account will be suspended in 3 business days.",
    "CIMB Alert: Unusual transaction of RM 4,500 detected. Call 03-XXXX immediately.",
    "Hello, this is the underwriting department. Your credit card limit needs verification.",
    "Your Public Bank account is blocked due to security reasons. Click here to verify.",
    "AmBank here, you have an outstanding fee of RM 200, pay now to avoid legal action.",
    "Police report has been lodged against your ID, please contact us urgently.",
    "Your account is being used for illegal activities. Transfer funds to our secure account."
]

SAFE_PHRASES = [
    "Hi, are we still meeting for lunch at the office later?",
    "Could you please send the meeting minutes for the project?",
    "I have submitted the quarterly report to the management team.",
    "Just a reminder that our team building is scheduled for next Friday.",
    "Thank you for the update regarding the new system deployment.",
    "Hi, let's catch up on the client requirements later this evening.",
    "The courier has arrived at the lobby to drop off the parcel.",
    "I will be working from home today due to personal matters."
]

def generate_malaysian_dataset(num_each=10000):
    data = []
    # Generate 10,000 SCAM
    for _ in range(num_each):
        data.append({"text": random.choice(SCAM_PHRASES), "label": "SCAM"})
    # Generate 10,000 SAFE
    for _ in range(num_each):
        data.append({"text": random.choice(SAFE_PHRASES), "label": "SAFE"})
    
    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv("dataset/malaysia_scam_data.csv", index=False)
    print("✅ Created dataset/malaysia_scam_data.csv with 20,000 entries!")

if __name__ == "__main__":
    generate_malaysian_dataset()