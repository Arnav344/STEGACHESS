                                StegaChess 

 ABOUT THE PROJECT 

StegaChess is a secure communication project that combines cryptography, steganography, and chess to hide secret messages inside legal chess moves.

The main idea behind this project is simple: instead of sending an encrypted message directly, the message is first encrypted and then hidden inside a chess game (PGN format). To anyone else, it looks like a normal chess match, but the intended receiver can decode the hidden message only after passing multiple authentication checkpoints.

I built this project as a way to explore how cybersecurity concepts like encryption, authentication, integrity verification, and covert communication can be combined into something interactive and unique.


 Problem Statement

Traditional encrypted communication protects message content, but it still reveals that a secret message exists.

StegaChess tries to solve this by:

* Encrypting the message using AES
* Hiding ciphertext inside chess moves
* Verifying receiver authenticity through checkpoint-based authentication
* Detecting tampering using SHA-256 hashing

This creates a secure and stealthy communication system.

 Features

* AES-based message encryption
* Chess move steganography using PGN
* Shared secret authentication key
* Checkpoint-based receiver verification
* Integrity verification using SHA-256 hashes
* Breach logging for failed authentication attempts
* Interactive chess GUI using Tkinter
* Receiver can decode message only after successful authentication

---

 Tech Stack

* Python
* Tkinter (GUI)
* python-chess (Chess logic and PGN handling)
* Pillow (Chess piece rendering)
* Cryptography library(AES encryption)
* SHA-256 hashing (Integrity verification)


Project Workflow

SENDER SIDE :

1. Sender enters:

   * Secret Message
   * Authentication Key
   * AES Key

2. Message gets encrypted using AES.

3. Ciphertext is converted into binary.

4. Binary chunks are mapped to legal chess moves.

5. Encoded PGN file and checkpoint data are generated.


RECIEVER'S SIDE :

1. Receiver enters authentication key.

2. System verifies the key.

3. Receiver must pass checkpoint authentication by playing required chess moves.

4. If authentication succeeds, receiver enters AES key.

5. Message gets decrypted and revealed.



SECURITY LAYER USED 

This project uses multiple security layers:

 1. Encryption Layer

AES encryption protects message confidentiality.

 2. Steganography Layer

Message is hidden inside a chess game.

 3. Authentication Layer

Only intended receiver with correct authentication key can proceed.

 4. Integrity Layer

SHA-256 hash ensures files were not tampered with.



 Folder Structure

StegaChess/
│
├── assets/
├── auth/
├── crypto/
├── engine/
├── gui/
├── README.md
├── requirements.txt
└── .gitignore



 Future Improvements

Some planned improvements for future versions:

* Single `.stg` sharable file format
* Dedicated desktop application
* Send / Receive interface
* One-click file sharing
* Better UI/UX
* Possible mobile app version



Why I Built This

Most secure communication projects focus only on encryption. I wanted to build something more creative that combines cybersecurity with strategic gameplay.

Chess naturally provides a large search space of legal moves, making it an interesting medium for covert communication.

This project helped me explore practical applications of:

* Cryptography
* Steganography
* Authentication systems
* GUI development
* Secure protocol design

CHESSBOARD GUI
![alt text](<Screenshot 2026-07-01 202625.png>)

AUTHENTICATION DIALOGUE BOX 
![alt text](<Screenshot 2026-07-01 202932.png>)

ENCRYPTION DIALOGUE BOX (AES)
![alt text](<Screenshot 2026-07-01 202949.png>)

CHECKPOINT PASSED 
![alt text](<Screenshot 2026-07-01 203918.png>)

MESSAGE AFTER AUTHENTICATION 
![alt text](<Screenshot 2026-07-01 203150.png>)
