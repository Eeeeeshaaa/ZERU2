# ZERU2
-----------DATA COLLECTION METHOD-------------
I collected on-chain wallet data by querying a blockchain analytics API that provides detailed transaction and lending information related to Aave V2/V3 protocols. Specifically , I fetched key metrics such as total collateral, borrow amounts , etc for each wallet under analysis.


-----------FEATURE SELECTION RATIONALE----------
1.Total borrows- Indicates how much a wallet has borrowed.
2.Total collateral- shows secuirt level
3.Health factor-It measures the safety margin of the loan
4.Available borrows-Shows unused borrowing capacity.


-----------SCORING METHOD-----------------------
I normlaised the key-risk related factors using min-max scaling to bring them into a comparable range. The risk score was computed as a weighted of these normalised features with higher weights assigned to total borrow amount and health factor inversion.



--------------APPROACHES---------------
I used this one because the error was shown when the code was done seperately for all other ones. I have used two approaches but both gave similar results.


----------JUSTIFICATION-----------
1.Total borrows- Large amounts increase risk exposure and potensial loss.
2.Health factor(inverted)-Measures the proximity to liquidation.
<img width="407" height="157" alt="image" src="https://github.com/user-attachments/assets/3d6ed832-097f-45a6-aba0-f6dd34596513" />
