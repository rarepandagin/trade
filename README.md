
trades should be performed on the DEX that offers a better slippage.
live slippage values for different trade sizes on different DEXes need to be available at all times.



# PAIRS
all trades has two parts to it: short and long
long parts works with the added collateral at the time of placing the order
short part works with the borrowed amount

note that there always remains a substantial amount of collateral in AAVE contract such
that we can always supply and withdraw collaterals without worrying for the 70% loan 
to collateral ratio

for every trade:
- certain amount of collateral is supplied (as for the long side)
- certain amount of weth is borrowed (as for the short side)

collateral / borrowed  ratio defines the bias of the trade

if the trade is long-biased, the ratio is larger than 1
this means that we believe that the price will go up

if the the trade is short-biased, the ratio is smaller than 1
this means that we believe that the price will go down


---- long-biased trade

In a long-biased trade, we consider a larger added collateral 
and a smaller borrow.

if the price goes up, the added collateral
generates more profit than the loss made from the borrow. 


if the price goes down, the added collateral
causes more loss than the profit made by the short. 

so, compared to stop loss of the short side, the stop loss for the long side should be placed closer to the entry price.




---- short-biased trade

In a short-biased trade, we consider a borrow and a smaller added collateral.

if the price goes up, the borrow generates more loss and the profit from the
added collateral.

if the price goes down, the borrow generates more profit that the lost made
by the added collateral.

therefore, compared to the stop loss for the long side, the stop loss for the short side
should be placed closer to the entry price.



the long side, does not need to be added collateral
you can just simply buy weth
but, you need to always maintain a fixed and constant amount of collateral







place the SL of the hedge at a bit after TP of the main asset
reasons:
    - making sure we always remain hedged until the main asset exists
    - there is tiny change that after the main asset exits, the price turns to the side of the hedge asset. in this case, which is rare, we don't need to exit the hedge position and realize the losses.
    - the extra loss amount is small and acceptable.
    

allow the PT of the hedge to go (on the wrong direction) further than the SL of the main asset.

adjust the hedging ratio considering for the time when the price ends up going the wrong way
adjust the hedging ratio such that the at the exit point of the hedge, the total profit is zero or small


adjust the SL of the main asset to a price at which you can confirm a market shift.
because at that price, we can only make profit if the market has shifted and goes toward our hedge.
otherwise, also the hedge will start generating losses. this is the worst case scenario.

