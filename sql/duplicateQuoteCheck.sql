SELECT text, COUNT(*) occurances FROM quote GROUP BY text HAVING occurances > 1;
