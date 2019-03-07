from searchtweets import load_credentials, ResultStream, gen_rule_payload, collect_results

premium_search_args = load_credentials("/twitter_keys.yaml",
                                       yaml_key="search_tweets_premium_example",
                                       env_overwrite=False)

# Testing with sandbox

rule = gen_rule_payload("حجاج العجمي",
                        from_date="2011-01-01",
                        to_date="2018-12-31",
                        results_per_call=100,
                        )# testing with a sandbox account
print(rule)

tweets = collect_results(rule,
                         max_results=100,
                         result_stream_args=premium_search_args) # change this if you need to
f = open("result.txt", "w+")

[print(tweet.all_text, end='\n\n') for tweet in tweets[0:50]];

