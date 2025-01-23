# Skin_Care_Recommendation Data Demo

TBD.....

ReadMe file for skin care recommendation project

- An overview of your dataset
What does it include?
Where and how will you be obtaining it? Include the link and source. If you plan on creating a web scraper or using an API, describe your plans.
About how many observations? How many predictors?
What types of variables will you be working with?
Is there any missing data? About how much? Do you have an idea for how to handle it?

Skincare API: https://proxyempire.io/scraping-api-for-lookfantastic/

We will utilize a Skincare API and our own custom-built web scraper using Python to compile a dataset of skin care products and their detailed characteristics, including:
→ Product details: Name, category (cleanser, moisturizer, etc.),
→ Skin-care ingredients 
→ Skin Types: Dry, Oily, Combination 
→ Prices: $, $$, $$$
→ Product URL: Product website

We’re aiming for multiple thousands of observations, and 6-10 predictors, and the variables we will handle include the above-mentioned characteristics (product details, skin-care ingredients, skin types, prices, product URL, etc.). There will be no missing data!

Our primary goal is to recommend users skincare products with ingredients similar to those of a product users input into our system. These will increase cleansers, moisturizers, serums, and treatments formulated with high-quality ingredients to address various skin concerns and provide effective solutions for different skin types.

- An overview of your research question(s)
What variable(s) are you interested in predicting? What question(s) are you interested in answering?
Name your response/outcome variable(s) and briefly describe it/them.
Which predictors do you think will be especially useful?
Is the goal of your model descriptive, predictive, inferential, or a combination? Explain.

Our research questions are:
→ Which skincare products best suit a user’s unique skin type, concerns, and preferences based on their input?
→ Which ingredients are best for specific skin types or most similar to the product the user inputted?

The variable of primary interest in our dataset is recommended skincare products, tailored to the user’s input. Our recommendation system will generate a list of products that align with the user’s preferences, skin types and concerns. Predictors especially useful will be ingredients, skin type, skin concerns, and the product prices. The goal of our system will be a combination of predictive (recommend products that meet user’s preferences based on their input) and descriptive (compare product ingredients and prices for best skin suitability).

- When do you plan on having your data set loaded, beginning your exploratory data analysis, etc? Provide a general timeline for the rest of the quarter.

Our group is in the process of accessing data from a skincare product API, and we anticipate some difficulty relating to APIs. By week 6 we hope to begin with EDA on the data which should help to understand how we can use the data for a recommender system. After week 8 our group hopes to have recommendations for every observation in the data, and we will likely spend the next couple of weeks refining the model to optimize results. By the end of week 10, we will hopefully have an accurate recommendation system for the skincare products. 

- Are there any problems or difficult aspects of the project you anticipate? Any specific questions you have for me/the instructional team?

We don’t have much experience in scraping from APIs, which may lead to data collection difficulties. Recommender systems are also new to our group, so developing a model could be difficult as well. 

