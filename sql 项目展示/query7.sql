SELECT COUNT(DISTINCT category_id) FROM Includes where item_id IN(
        SELECT DISTINCT bid_item 
        FROM Bid
        WHERE Bid.amount > 100)