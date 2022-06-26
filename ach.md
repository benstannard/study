2022 Jun 25
[source](https://squareup.com/us/en/townsquare/ach-payments)

# Quick ACH fact sheet:
+ **Applicable Accounts**: Checking and savings accounts only
+ **Areas of operation**: United States and Puerto Rico
+ **Governing body**: NACHA (The Electronic Payment Association)
+ **Typical processing times**: Fund become available within about 3-5 business days

#### Benefits
Lower processing costs, fewer declines due to expiration (checking accounts don't expire like CC/Debit Cards), Less paper invoices, checks and trips to the bank, more convenient for customers "set it and forget it"

#### Drawbacks
Speed (can take several days), Caps ($25,000 same day), Cutoff times (after a later Friday, won't be processed until Monday), US only.

# What is an ACH Payment?
ACH = Automated Clearing House, a U.S financial network used for electronic payments and money transfers. Also known as **direct payments**. ACH payments are a way to transfer money from one bank account to another without using paper checks, credit card networks, wire transfers or cash.  

ACH payment volume is steadily growing. ACH network processed more than 25 billion electronic payments, totalling over $43 trillion in 2015.  

As a consumer, you are probably using the ACH network even though you might now be aware:
+ if you pay your bills electronically (instead of writing a check or entering a credit card number)
+ recieve direct deposit from your employer

For **businesses**, ACH payments are popular alternative to paper check and credit card payments. Because they are electronic, ACH payments are faster, and more reliable than checks, helping automate and streamline accounting. Generally, it also costs less to process and ACH transfer than a CC payment or wire transfer. If you're a business that accepts recurring payments, the savings can be significant.

# What's the difference between ACH payments, wire transfers, and EFT payments?
While ACH payments and wire transfers are both ways to move money between two accounts, there are a number of differences between them.
+ Wire transfers are processed in real time, as opposed to ACH payments, which are processed in batches three times a day. As a result, Wire Transfers are guaranteed to arrive on the same day, while ACH funds can take several days to process.
+ Wire transfers are also more expensive than ACH payments, while some banks don't charge for wires, others can cost $60

**ETF** payments (Electronic funds transfer) can be used interchangeably with ACHO payments. They both describe the same payment mechanism.

# Examples of ACH payments
There are two times of ACH payments:
1. ACH debits transactions involve money being **"pulled"** from your account. Must be processed the next business day.
2. ACH credit transactions let you **"push"** money to different banks (either your own or to others). Can be processed within or in one or two days.

#### Direct Depost Payroll
Many companeis offer direct deposit payroll. They use ACH credit transactions to **push** money to their employees bank accounts at designated pay periods. (Employees need to provide a voided check or a checking account and routing number to set this up).

#### Recurring Bill Payments
Consumers who pay a business (insurance, mortgage lender) at certain intervals may choose to sign up for *recurring payments*. That gives the business the ability to initiate ACH debit transactions at each billing cycle, **pulling** the amount owed directly from the consumer's account.

# How ACH payments work
Aside from the Automated Clearing House network (which connects all the banks in the US) there are three other players involved in ACH payments:
- **ODFI** The Originating Depository Financial Institution is the banking instituion that initiates the transaction
- **RDFI** The Receiving Depository Financial Institution is the banking institution that receives the ACH request
- [**NACHA**](https://www.nacha.org/) is the nonpartisan governmental entity responsible for overseeing and regulating the ACH network.

### So how do ACH Payments work?
Let's take your automated monthly phone bill payment. When you sign up for **autopay** with your phone company, you provide your checking account information (routing and account number) and sign a recurring payment authorization.  

Then, when you hit your billing cycle, your phone company's bank (the ODFI) sends a request to your bank (the RDFI) to transfer the money owed. The two banks then communicate to ensure that there are enough funds in the bank account to process the transaction.  

If you have sufficent funds, the transaction is processed and the money is routed to your phone company's bank account.  

# What are typical ACH payment processing times?
ACH payments typically take several business days (the days on which banks are open) to go through. The ACH network processes payments in **batches** as opposed to wire transfers, which are processed in real time.  

Per NACHA, FI can chose to have ACH credits processed and delivered either winin a business day or in one to two days. ACH debits must be processed by the next business day.  

After recieving the transfer, the other bank may also detain the transferred funds for a holding period.

# How much do ACH payments cost to process?
ACH payments are typically more affordable for business to process than credit cards. Your merchant account provider (or whatever entity you're using to process ACH payments) sets the price. Some ACH processors charge a flat rate, $.25-.75. Others may charge .5-1% per transaction.

# Why are some ACH payments rejected?
If an ACH payment is rejected, your bank (OFDI) will provide a reject code that explains what happened. These reject codes are important for providing the right information to your customers as to why their payment didn't go through. Here are 4 most common reject codes:
1. **R01 Insufficent funds.** Customer didn't have enough money in their account to cover the amount of the debit entry. Add money or new payment method
2. **R02 Bank account closed.** Customer closed an active account and likely forgot to notify you of the change.
3. **R03 No bank account/unable to locate** Some combination of the data given doesn't match the banks records or a nonexistent account number was entered.
4. **R29 reject** If a bank doesn't allow a business to withdraw funds from a particular bank account, you'll get this code. They need to provide their bank with your ACH Originator ID to enable ACH withdraawls by your business.

# Are there any penalty fees with ACH payments?
Unfortunately, rejected ACH payments could land your business a penalty fee. So if you get a reject code, it's important to quickly correct the issue to avoid incurring additional fees on each recurring billing cycle. It may be worth only accepting ACH payments from trusted customers.

# ACH security
Although the ACH network is managed by the federal government and NACHA, ACH payments don't have to follow the same [PCI-compliance](https://squareup.com/us/en/townsquare/pci-compliance) required for credit card processing. However, NACHA requires that all parties involved in ACH transactions, including business initiating the payments and third-party processors, implement processes, procedures, and controls to protect sensitive data. NACHA stipulate that the transmission of any banking information be encrypted using "commerically reasonable" technology.  

That means you can't send or recieve bank information via **unencrypted email or insecure web forms**. Make sure that if you use a third party for ACH payment processing, it has implemented systems with state-of-the-art encryption methods.  

NACHA rules, originators of ACH payments must also take "commerically reasonable" steps to ensure the validity of customer identity and routing numbers, and to identify possible fradulent activity. Most third-party ACH processors should have these capabilities, but make sure to check before you sign on with anyone. 




