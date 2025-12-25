import re

def extract_valid_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    valid_emails = []
    for email in re.findall(pattern, text):
        if len(email) <= 30 and not email.endswith(('.png', '.jpg')):
            valid_emails.append(email)
    return valid_emails

def main():
    with open('validemails.txt', 'r') as file:
        text = file.read()
    
    valid_emails = extract_valid_emails(text)
    
    for email in valid_emails:
        print(email)

if __name__ == "__main__":
    main()
