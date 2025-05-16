# class CodexREPL:
#
#     def __init__(self):
#         self._client = PerplexityClient(key = os.environ['PERPLEXITY_API_KEY'])
#         self._client.model = DEFAULT_MODEL_NAME
#         self._queryCodeStyle = True
#         self._editingMode = EditingMode.VI
#
#
#     def core(self, userQuery: str) -> str:
#         """
#         Send a user query to the model for processing.
#
#         Arguments
#         ---------
#             userQuery
#         A string with the user query, most often a programming question.
#
#         Returns
#         -------
#         The result of the query, or `None` if the query was empty.
#         """
#         result = None
#         userQuery = userQuery.strip()
#         if userQuery:
#             if not self._client:
#                 self._client = PerplexityClient(key = os.environ['PERPLEXITY_API_KEY'])
#                 self._client.model = DEFAULT_MODEL_NAME
#             result = self._client.query(userQuery)
#
#         return result
#
#
#     def activeModel(self, modelID: int = 0) -> str:
#         if modelID:
#             try:
#                 ref = modelID-1
#                 model = list(self._client.models.keys())[ref]
#                 self._client.model = model
#             except:
#                 click.secho('Invalid model ID = %s' % modelID, bg = 'red', fg = 'white')
#         click.secho('Active model: %s\n' % self._client.model, fg = 'green', bold = True)
#         return self._client.model
#
#
#
#     def displayModels(self) -> list:
#         """
#         Display the list of models supported by the API.
#
#         Returns
#         =======
#         A list of strings, each corresponding to a model name.
#         """
#         self.activeModel()
#         print('Available models:\n')
#         n = 1
#         for model in self._client.models.keys():
#             print('%2d - %s' % (n, model))
#             n += 1
#         print()
#
#         return list(self._client.models.keys())
#
#
#     def editingMode(self, session: PromptSession, mode: str = None) -> PromptSession:
#         """
#         Sets the editing mode to `vi` or `emacs`.
#
#         Arguments
#         =========
#             session
#         An instance of `PromptSession` from the current Click hosting.
#
#             mode
#         A string with the values of 'vi' or 'emacs'; any other value is
#         overriden with `vi`.
#
#         Returns
#         =======
#         An updated PromptSession instance that with the value of `mode`.
#         """
#         if mode:
#             mode = mode.lower()
#             self._editingMode = EditingMode.EMACS if mode == 'emacs' else EditingMode.VI
#             session = PromptSession(editing_mode = self._editingMode)
#
#         editingMode = str(session.editing_mode).replace('EditingMode.', '').lower()
#         click.secho('Editing mode = %s' % editingMode, fg = 'bright_blue')
#
#         return session
#
#
#     @property
#     def queryCodeStyle(self) -> bool:
#         """
#         Return `True` if the current style is code, `False` for human.  The object uses
#         this Boolean value to determine the type of query to execute.  Future
#         versions may use the words `code` or `human`, or perhaps an enum with
#         those values.
#         """
#         return self._queryCodeStyle
#
#
#     @queryCodeStyle.setter
#     def queryCodeStyle(self, newStyle: str = None) -> bool:
#         """
#         Set the receiver query code style to `newStyle`.  Code style queries
#         generate responses that include code snippets in Python or JavaScript,
#         and URLs to references that show how to address the query topic.
#         `human` style queries produce textual, prose responses that address the
#         query topic in detail, and may or may not contain code, even if the
#         query was about a programming concept.
#
#         The method will default to `code` style for any value of `newStyle` that
#         isn't `code`.
#
#         Arguments
#         =========
#             `newStyle`
#         A string with either value of 'code' or 'human'.
#
#         Returns
#         =======
#         `True` if the current style is code, `False` for human.  The object uses
#         this Boolean value to determine the type of query to execute.  Future
#         versions may use the words `code` or `human`, or perhaps an enum with
#         those values.
#         """
#         if newStyle:
#             self._queryCodeStyle = newStyle != 'human'
#         click.secho('Coding query style = %s' % self._queryCodeStyle, fg = 'bright_blue')
#
#
#     def makeQuery(self, userQuery: str) -> str:
#         """
#         Execute a query using the `PerplexityClient` and return the result in
#         a string.
#
#         Arguments
#         =========
#             userQuery
#         A free from, natural language string describing the request to the AI
#         provider.
#
#         Returns
#         =======
#         The response from the AI/LLM.
#
#         Raises
#         ======
#         `ValueError` if `userQuery` is `None` or an empty string.
#         """
#         if not userQuery:
#             raise ValueError('userQuery string cannot be empty')
#         if self._queryCodeStyle:
#             userQuery = QUERY_DETAILED+userQuery
#
#         return self.core(userQuery)
#
#
#     def _saveConfigTo(self, config: dict, fileName: str = CONFIG_FILE_NAME, pathName = CONFIG_PATH):
#         if not os.path.exists(pathName):
#             os.makedirs(pathName)
#         with open(fileName, 'w') as outputFile:
#             yaml.dump(config, outputFile)
#
#
#     def _loadConfigFrom(self, fileName: str = CONFIG_FILE_NAME, pathName = CONFIG_PATH) -> dict:
#         if os.path.exists(fileName):
#             with open(fileName, 'r') as inputFile:
#                 config = yaml.safe_load(inputFile)
#         else:
#             # TODO:  turn this into a self-contained object; maybe a named
#             #        tuple?
#             config = {
#                 'activeModel': DEFAULT_MODEL_NAME,
#                 'editingMode': 'vi',
#                 'queryCodeStyle': _queryCodeStyle,
#             }
#             _saveConfigTo(config, fileName, pathName)
#         return config
#
#
#     def _displayConfigInfo(self):
#         click.secho('Config file: %s' % CONFIG_FILE_NAME)
#         click.secho(str(_loadConfigFrom())+'\n')
#
#
#     def run(self):
#         pass
#
#
#
