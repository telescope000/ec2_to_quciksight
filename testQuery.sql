SELECT region, SUM(qty*price) AS total_sales
FROM starshop.orders
GROUP BY region
ORDER BY total_sales DESC; 
