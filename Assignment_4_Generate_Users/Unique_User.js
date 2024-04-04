// Importing required modules
const webdriver = require('selenium-webdriver');
const By = webdriver.By;
const Key = webdriver.Key;
const ActionSequence = webdriver.ActionSequence;
const natural = require('natural');
const TfIdf = natural.TfIdf;
const tfidf = new TfIdf();
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const random = require('random');

// User action function
async function userAction(action, driver, reward_time, req_list) {
    let total_reward_time = 0;
    if (action.toUpperCase() === "KEYWORD") {
        if(req_list) {
            for (let keyword of req_list) {
                console.log("found", keyword);
                let num_words = await findKeyword(driver, keyword);
                console.log("appeared", num_words, "times");
                let reward_time_X = reward_time * num_words;
                await sleep(reward_time_X);
                total_reward_time += reward_time_X;
            }
        } else {
            console.log("Program decided to not choose any word for keyword (this is not a bug)...");
        }
    } else if (action.toUpperCase() === "IMAGE") {
        let item = await countElem(driver, req_list);
        let num_images = item[0];
        let reward_time_X = reward_time * num_images;
        total_reward_time = reward_time_X;
        console.log("# of Images: ", num_images);
        await sleep(reward_time_X);
    } else if (action.toUpperCase() === "LINK") {
        let item = await countElem(driver, req_list);
        let num_links = item[0];
        await clickLinks(driver, item[1]);
        let reward_time_X = reward_time * num_links;
        total_reward_time = reward_time_X;
        console.log("# of Links: ", num_links);
        await sleep(reward_time_X);
    }
    return total_reward_time;
}

// Find keyword function
async function findKeyword(driver, keyword) {
    // Get the page source HTML
    let page_source = await driver.getPageSource();

    // Parse the HTML using JSDOM
    let dom = new JSDOM(page_source);
    let document = dom.window.document;

    // Find all visible text elements on the page
    let visible_text = Array.from(document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li')).map(element => element.textContent.toLowerCase());

    // Create a regular expression pattern to match whole words
    let pattern = new RegExp(`\\b${keyword.toLowerCase()}\\b`, 'g');

    // Count the keyword in visible text
    let num_occurrences = visible_text.reduce((count, text) => count + (text.match(pattern) || []).length, 0);

    return num_occurrences;
}

// Count element function
async function countElem(driver, tag_name) {
    // Get count of elements for the specified tag_name
    let elements = await driver.findElements(By.tagName(tag_name));
    
    // Total number of elements
    let total_length = elements.length;

    // Randomly select how many elements you are interested in
    let num_elements_of_interest = random.int(1, total_length);  // Randomly select a number from 1 to total_length
    
    // Randomly select a subset of elements
    let elements_of_interest = random.sample(elements, num_elements_of_interest);

    return [num_elements_of_interest, elements_of_interest];
}

// Click links function
async function clickLinks(driver, links) {
    // Find link or links and click on them....
    for (let link of links) {
        let action = new ActionSequence(driver);
        action.keyDown(Key.SHIFT);
        action.click(link);
        action.keyUp(Key.SHIFT);
        await action.perform();
    }
}

// Sleep function
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Skim paragraphs function
async function skimParagraphs(driver) {
    // Find all paragraphs
    let paragraphs = await driver.findElements(By.tagName("p"));
    
    // Extract the text of each paragraph
    let p_contents = await Promise.all(paragraphs.map(async (paragraph) => {
        return (await paragraph.getText()).toLowerCase();
    }));

    // Filter out stop words
    let stop_words = new Set(stopwords.en);

    let filtered_contents = [];
    for (let content of p_contents) {
        let words = content.split();
        let filtered_words = words.filter(word => !stop_words.has(word));
        filtered_contents.push(filtered_words.join(' '));
    }

    // Apply tf-idf to the paragraphs
    tfidf.addDocuments(filtered_contents);

    // Get the words
    let words = tfidf.listTerms(0 /* in document index 0 */).map(term => term.term);

    // Get the frequency of each word
    let word_frequencies = words.map(word => tfidf.tfidf(word, 0));

    // Create a dictionary of words and their frequencies
    let word_frequency_dict = {};
    for (let i = 0; i < words.length; i++) {
        word_frequency_dict[words[i]] = word_frequencies[i];
    }

    // Sort the dictionary by value (frequency) in ascending order
    let sorted_word_frequency_dict = {};
    Object.keys(word_frequency_dict).sort((a, b) => {return word_frequency_dict[a] - word_frequency_dict[b]}).forEach(function(key) {
        sorted_word_frequency_dict[key] = word_frequency_dict[key];
    });

    console.log(sorted_word_frequency_dict);
    return sorted_word_frequency_dict;
}

// Keyword select function
function keywordSelect(dictionary) {
    // Convert the dictionary to a list of tuples
    let items = Object.entries(dictionary);

    // Determine the number of keywords to select
    let num_keywords = random.int(0, 2);

    if(num_keywords != 0) {
        // Determine the discrimination factor
        let discrimination_factor = random.float(0, Math.max(...Object.values(dictionary)));

        console.log();
        console.log("Level of Reader Interest Factor: ", discrimination_factor);
        console.log("Going to remove words lower than this factor");
        console.log("This is how many keywords I will care about: ", num_keywords);
        console.log();

        // Filter the items based on the discrimination factor
        let filtered_items = items.filter(item => item[1] >= discrimination_factor);

        // If the discrimination factor is too high and no items are left, use last item
        if (!filtered_items.length) {
            filtered_items = items;
        }

        console.log("This is the list dictionary after removal");
        console.log(filtered_items);

        // Randomly select keywords
        let selected_keywords = random.sample(filtered_items, Math.min(num_keywords, filtered_items.length));

        // Return the selected keywords
        return selected_keywords.map(item => item[0]);
    }
    return [];
}

// Main function
async function main() {
    // Initialize browser
    let driver = new webdriver.Builder().forBrowser('chrome').build();

    // Navigate to your website
    await driver.get("http://localhost:3000");

    let tfidfDictionary = await skimParagraphs(driver);
    let reward_time = 10;
    let total_reward_time = await userAction("KEYWORD", driver, reward_time, keywordSelect(tfidfDictionary));
    total_reward_time += await userAction("IMAGE", driver, reward_time, "img");
    total_reward_time += await userAction("LINK", driver, reward_time, "a");

    await driver.quit();
    console.log("Presence Time:", total_reward_time);
}

// Run the main function
main();