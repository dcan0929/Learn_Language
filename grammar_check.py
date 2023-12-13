from language_tool_python import LanguageTool

def grammar_check_with_correction(text):
    tool = LanguageTool('en-US')
    matches = tool.check(text)

    grammar_errors_and_corrections = {}
    for match in matches:
        if match.ruleIssueType == 'grammar':
            grammar_errors_and_corrections[match.offset] = {
                'error': match.msg,
                'corrections': ', '.join(match.replacements)
            }

    return grammar_errors_and_corrections

user_input_grammar = input("Enter a sentence: ")

grammar_errors_and_corrections = grammar_check_with_correction(user_input_grammar)
if not grammar_errors_and_corrections:
    print("No grammar errors.")
else:
    print("Grammar errors and corrections:")
    for offset, data in grammar_errors_and_corrections.items():
        print(f"At position {offset}: {data['error']}")
        print(f"Correction suggestions: {data['corrections']}")
