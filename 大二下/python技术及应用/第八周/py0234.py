def printTable(data):
    # Determine the number of columns from the length of the first sub-list
    num_columns = len(data[0])

    # Initialize colWidths with zeros, one for each column
    colWidths = [0] * num_columns

    # Loop through each column and find the maximum width of items in that column
    for column in zip(*data):
        for i, item in enumerate(column):
            colWidths[i] = max(colWidths[i], len(item))

    # Print the table, each word is left-justified to the column width
    for row in zip(*data):
        for i, word in enumerate(row):
            print(word.ljust(colWidths[i]), end=' ')
        print()

# Data for the table
tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose']]

# Call the function to print the table
printTable(tableData)
