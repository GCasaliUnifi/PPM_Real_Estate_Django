from django import template

register = template.Library()


# This custom filter is used to truncate the description of the listing after a certain number of words.
# Useful when you want to display a short description of the listing on the homepage or elsewhere.
@register.filter
def truncate_words(value, num_words):
    words = value.split()
    if len(words) <= num_words:
        return value
    else:
        truncated_words = words[:num_words]
        return " ".join(truncated_words) + "..."


#
# Truncates a string after a certain number of characters, including spaces.
# Usage: {{ value|cut_after_chars:arg }}
# Example: {{ listing.description|cut_after_chars:100 }}
# This filter is better tha truncate_words because it will also cut if someone enters a long string without spaces.
#
@register.filter
def cut_after_chars(value, arg):
    if len(value) <= arg:
        return value

    words = value.split()
    result = ""
    count = 0
    for word in words:
        count += len(word) + 1 # +1 for the space after each word
        if count > arg:
            result += "..."
            break
        result += word + " "

    return result.strip() # remove the last space
