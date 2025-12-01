@@ -6,13 +6,12 @@
 from exa_py import Exa
 import anthropic
 from datetime import datetime, timedelta
-import os
 
 # Page config
 st.set_page_config(
     page_title=""Stock Analysis Assistant"",
     page_icon=""📈"",
-    layout=""wide""
+    layout=""wide"",
 )
 
 # Initialize session state for conversation
@@ -23,7 +22,7 @@
 
 # Title and description
 st.title(""Stock Analysis Assistant"")
-st.markdown(""Get comprehensive investment analysis using AI and real-time data."")
+st.markdown(""Get investment analysis using AI and real-time data."")
 
 # Sidebar for API keys
 with st.sidebar:
@@ -37,16 +36,15 @@
     {
         ""name"": ""yahoo_finance"",
         ""description"": (
-            ""Fetches current stock data for a given ticker from Yahoo Finance. ""
-            ""Provides real-time pricing, volume, and market trends. ""
-            ""Use this tool when you need quantitative data about a stock.""
+            ""Fetches stock data from Yahoo Finance. ""
+            ""Provides pricing, volume, and market trends.""
         ),
         ""input_schema"": {
             ""type"": ""object"",
             ""properties"": {
                 ""ticker"": {
                     ""type"": ""string"",
-                    ""description"": ""The stock ticker symbol (e.g., TSLA for Tesla, Inc.)""
+                    ""description"": ""Stock ticker symbol""
                 }
             },
             ""required"": [""ticker""]
@@ -55,8 +53,8 @@
     {
         ""name"": ""perplexity_news"",
         ""description"": (
-            ""Fetches recent news and financial reports for a given stock ticker using the Perplexity API. ""
-            ""Use this tool to retrieve the latest headlines and summaries related to the stock.""
+            ""Fetches recent news and reports using Perplexity API. ""
+            ""Retrieves latest headlines and summaries.""
         ),
         ""input_schema"": {
             ""type"": ""object"",
@@ -72,8 +70,8 @@
     {
         ""name"": ""exa_search"",
         ""description"": (
-            ""Performs a detailed search for financial news and reports on a given stock ticker using the Exa AI Search API. ""
-            ""Use this tool when you need to fetch comprehensive search results, including reports within a specific date range.""
+            ""Searches for financial news using Exa AI Search API. ""
+            ""Fetches comprehensive results within date range.""
         ),
         ""input_schema"": {
             ""type"": ""object"",
@@ -84,15 +82,15 @@
                 },
                 ""start_date"": {
                     ""type"": ""string"",
-                    ""description"": ""The start date for the search in ISO format.""
+                    ""description"": ""Start date in ISO format""
                 },
                 ""end_date"": {
                     ""type"": ""string"",
-                    ""description"": ""The end date for the search in ISO format.""
+                    ""description"": ""End date in ISO format""
                 },
                 ""num_results"": {
                     ""type"": ""integer"",
-                    ""description"": ""The number of search results to return."",
+                    ""description"": ""Number of results to return"",
                     ""default"": 5
                 }
             },
@@ -102,35 +100,40 @@
     {
         ""name"": ""calculator"",
         ""description"": (
-            ""A simple calculator that performs basic arithmetic operations. ""
-            ""Use this tool to perform any necessary calculations.""
+            ""Performs basic arithmetic operations. ""
+            ""Use for numerical calculations.""
         ),
         ""input_schema"": {
             ""type"": ""object"",
             ""properties"": {
                 ""expression"": {
                     ""type"": ""string"",
-                    ""description"": ""The mathematical expression to evaluate (e.g., '2 + 3 * 4').""
+                    ""description"": ""Mathematical expression to evaluate""
                 }
             },
             ""required"": [""expression""]
         }
     }
 ]
 
+
 def fetch_yahoo_finance(ticker):
     """"""Fetches last week's market data for a given ticker using yfinance.""""""
     try:
         stock = yf.Ticker(ticker)
         hist = stock.history(period=""7d"")
         if hist.empty:
-            return f""Yahoo Finance: No market data found for {ticker} in the last week.""
-        return f""Yahoo Finance: Last week's market data for {ticker}:
{hist.to_string()}""
+            msg = f""Yahoo Finance: No data for {ticker} in last week.""
+            return msg
+        data = hist.to_string()
+        return (f""Yahoo Finance: Last week's data for {ticker}:""
+                f""
{data}"")
     except Exception as e:
         return f""Error fetching Yahoo Finance data: {e}""
 
+
 def fetch_perplexity_news(ticker, api_key):
-    """"""Calls the Perplexity Chat Completions API to fetch recent news headlines for a ticker.""""""
+    """"""Calls Perplexity API to fetch recent news headlines.""""""
     url = ""https://api.perplexity.ai/chat/completions""
     headers = {
         ""Authorization"": f""Bearer {api_key}"",
@@ -140,7 +143,8 @@ def fetch_perplexity_news(ticker, api_key):
         ""model"": ""sonar"",
         ""messages"": [
             {""role"": ""system"", ""content"": ""Be precise and concise.""},
-            {""role"": ""user"", ""content"": f""Provide the latest news headlines and summaries for {ticker}.""}
+            {""role"": ""user"",
+             ""content"": f""Provide latest headlines for {ticker}.""}
         ],
         ""max_tokens"": 500,
         ""temperature"": 0.2,
@@ -155,22 +159,22 @@ def fetch_perplexity_news(ticker, api_key):
         response = requests.post(url, json=payload, headers=headers)
         if response.status_code == 200:
             data = response.json()
-            answer = data.get(""choices"", [{}])[0].get(""message"", {}).get(""content"", """")
-            return f""Perplexity News: {answer}""
+            msg = data.get(""choices"", [{}])[0]
+            content = msg.get(""message"", {}).get(""content"", """")
+            return f""Perplexity News: {content}""
         else:
-            return f""Error fetching Perplexity news: {response.text}""
+            return f""Perplexity API error: {response.text}""
     except Exception as e:
         return f""Exception in Perplexity API call: {e}""
 
+
 def fetch_exa_search(ticker, start_date, end_date, api_key, num_results=5):
     """"""Uses the Exa AI Search API to retrieve financial news and reports.""""""
     try:
         exa = Exa(api_key=api_key)
-        query = f""financial news and reports on {ticker}""
+        query = f""financial news on {ticker}""
         result = exa.search_and_contents(
-            query,
-            text=True,
-            num_results=num_results,
+            query, text=True, num_results=num_results,
             start_published_date=start_date,
             end_published_date=end_date,
             include_text=[ticker]
@@ -183,54 +187,63 @@ def fetch_exa_search(ticker, start_date, end_date, api_key, num_results=5):
                 if not title:
                     title = getattr(res, ""url"", ""No title"")
                 headlines.append(title)
-            return f""Exa Search: Found {len(headlines)} results: "" + "", "".join(headlines)
+            results = "", "".join(headlines)
+            return f""Exa Search: {len(headlines)} results: {results}""
         else:
-            return f""Exa Search: No results found for {ticker} in the given period.""
+            return f""Exa Search: No results for {ticker} in given period.""
     except Exception as e:
         return f""Error fetching Exa Search results: {e}""
 
+
 def calculate(expression):
     """"""Evaluates a sanitized arithmetic expression.""""""
     expression = re.sub(r'[^0-9+-*/().]', '', expression)
     try:
         result = eval(expression)
         return str(result)
-    except (SyntaxError, ZeroDivisionError, NameError, TypeError, OverflowError):
+    except (SyntaxError, ZeroDivisionError, NameError,
+            TypeError, OverflowError):
         return ""Error: Invalid expression""
 
+
 def process_tool_call(tool_name, tool_input, api_keys):
+    """"""Process tool calls and return results.""""""
     if tool_name == ""yahoo_finance"":
         return fetch_yahoo_finance(tool_input[""ticker""])
     elif tool_name == ""perplexity_news"":
-        return fetch_perplexity_news(tool_input[""ticker""], api_keys[""perplexity""])
+        ticker = tool_input[""ticker""]
+        api_key = api_keys[""perplexity""]
+        return fetch_perplexity_news(ticker, api_key)
     elif tool_name == ""exa_search"":
         ticker = tool_input[""ticker""]
         start_date = tool_input[""start_date""]
         end_date = tool_input[""end_date""]
         num_results = tool_input.get(""num_results"", 5)
-        return fetch_exa_search(ticker, start_date, end_date, api_keys[""exa""], num_results)
+        api_key = api_keys[""exa""]
+        return fetch_exa_search(
+            ticker, start_date, end_date, api_key, num_results
+        )
     elif tool_name == ""calculator"":
         return calculate(tool_input[""expression""])
     else:
         return f""Error: Unknown tool {tool_name}""
 
+
 # Main input form
 with st.form(""stock_analysis_form""):
-    ticker = st.text_input(""Enter stock ticker (e.g., TSLA)"").strip().upper()
-    
+    ticker = st.text_input(""Enter stock ticker"").strip().upper()
     col1, col2 = st.columns(2)
     with col1:
         start_date = st.date_input(
-            ""Start date for news search"",
+            ""Start date"",
             value=datetime.now() - timedelta(days=30)
         )
     with col2:
         end_date = st.date_input(
-            ""End date for news search"",
+            ""End date"",
             value=datetime.now()
         )
-    
-    submit_button = st.form_submit_button(""Analyze Stock"")
+    submit_button = st.form_submit_button(""Analyze"")
 
 # Process form submission
 if submit_button:
@@ -244,85 +257,73 @@ def process_tool_call(tool_name, tool_input, api_keys):
             ""perplexity"": perplexity_key,
             ""exa"": exa_key
         }
-        
         client = anthropic.Anthropic(api_key=anthropic_key)
-        
         system_prompt = (
-            ""You are an investment analysis assistant. Your task is to provide a comprehensive ""
-            ""investment assessment for a given stock. Use the following tools as needed:

""
-            ""1. yahoo_finance: To get real-time stock data (price, volume, trends).
""
-            ""2. perplexity_news: To fetch recent news headlines and financial reports about the stock.
""
-            ""3. exa_search: To perform an in-depth search for financial news and detailed reports within a specified date range.
""
-            ""4. calculator: To perform any arithmetic calculations required during your analysis.

""
-            ""Make sure to use the tools only when needed and incorporate their results into your final investment recommendation.""
-            ""When you are done stop using tools and just provide your final verdict!!!""
+            ""You are an investment assistant. Your task is to analyze and ""
+            ""assess the given stock. Use these tools:

""
+            ""1. yahoo_finance: Get stock data (price, volume)
""
+            ""2. perplexity_news: Fetch news headlines
""
+            ""3. exa_search: Search for financial news within date range
""
+            ""4. calculator: Perform arithmetic calculations

""
+            ""Use tools when needed and add results to your recommendation. ""
+            ""When done, provide your final verdict.""
         )
-        
         user_prompt = (
-            f""Please provide a comprehensive investment assessment for {ticker}. ""
-            ""Include an analysis of the current stock data, recent news, and any additional financial reports if available. ""
-            ""Use the available tools as needed: use 'yahoo_finance' for current market data, 'perplexity_news' for recent news, ""
-            ""'exa_search' for a detailed search over a specified date range, and 'calculator' for any necessary arithmetic. ""
-            ""Please make sure to use the calculator at least two times to generate accurate numerical results.""
+            f""Analyze investment potential for {ticker}. ""
+            ""Review market data and news. ""
+            ""Use APIs to gather info. ""
+            ""Use search and calculator for analysis. ""
+            ""Run calculator twice.""
         )
-        
         # Initialize conversation if empty
         if not st.session_state.conversation:
-            st.session_state.conversation = [{""role"": ""user"", ""content"": user_prompt}]
-        
+            st.session_state.conversation = [
+                {""role"": ""user"", ""content"": user_prompt}
+            ]
+
         # Create a placeholder for the analysis
         analysis_placeholder = st.empty()
-        
+
         with st.expander(""Analysis Progress"", expanded=True):
             while True:
                 response = client.messages.create(
                     model=""claude-3-sonnet-20240229"",
-                    system=system_prompt,
-                    max_tokens=4096,
-                    tools=tools,
-                    messages=st.session_state.conversation
+                    max_tokens=4096, system=system_prompt,
+                    tools=tools, messages=st.session_state.conversation
+                )
+                st.session_state.conversation.append(
+                    {""role"": ""assistant"", ""content"": response.content}
                 )
-                
-                st.session_state.conversation.append({
-                    ""role"": ""assistant"",
-                    ""content"": response.content
-                })
-                
                 tool_called = False
                 for block in response.content:
                     if block.type == ""tool_use"":
                         tool_called = True
                         tool_name = block.name
                         tool_input = block.input
-                        
-                        # Show tool call progress
-                        st.info(f""Using tool: {tool_name} with input: {json.dumps(tool_input)}"")
-                        
-                        result = process_tool_call(tool_name, tool_input, api_keys)
-                        st.success(f""Tool result: {result}"")
-                        
-                        tool_result_message = {
+
+                        # Show progress
+                        st.info(f""Using {tool_name}: {json.dumps(tool_input)}"")
+
+                        result = process_tool_call(
+                            tool_name, tool_input, api_keys
+                        )
+                        st.success(f""Result: {result}"")
+
+                        msg = {
                             ""role"": ""user"",
-                            ""content"": [
-                                {
-                                    ""type"": ""tool_result"",
-                                    ""tool_use_id"": block.id,
-                                    ""content"": result
-                                }
-                            ]
+                            ""content"": [{
+                                ""type"": ""tool_result"",
+                                ""tool_use_id"": block.id,
+                                ""content"": result
+                            }]
                         }
-                        st.session_state.conversation.append(tool_result_message)
+                        st.session_state.conversation.append(msg)
                         break
-                
                 if not tool_called:
-                    final_answer = """"
-                    for block in response.content:
-                        if block.type == ""text"":
-                            final_answer += block.text
-                    
-                    # Update the analysis placeholder with the final result
-                    analysis_placeholder.markdown(f""### Investment Analysis
{final_answer}"")
+                    final_answer = """".join(
+                        block.text for block in response.content
+                        if block.type == ""text"")
+                    analysis_placeholder.markdown(
+                        f""### Investment Analysis
{final_answer}"")
                     break
-        
-        # Clear conversation for next analysis
         st.session_state.conversation = []