Sub ExportAllTablesLocalSQLToCSV()
    Dim conn As Object
    Dim cat As Object
    Dim tbl As Object
    Dim rs As Object
    Dim strSQL As String
    Dim csvFolderPath As String
    Dim i As Integer, j As Integer
    
    ' Set the path to your local SQL file
    Dim dbPath As String
    dbPath = "C:\Users\RohitBhardwaj\Downloads\Data.sql" ' Replace with the path to your local SQL file
    
    ' Set the folder path where CSV files will be saved
    csvFolderPath = "C:\Users\RohitBhardwaj\Downloads" ' Replace with your desired folder path
    
    ' Create a connection to the local SQL file using ACE OLEDB Provider
    Set conn = CreateObject("ADODB.Connection")
    conn.Open "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" & dbPath
    
    ' Create a Catalog object to access the tables in the database
    Set cat = CreateObject("ADOX.Catalog")
    cat.ActiveConnection = conn
    
    ' Iterate through all tables in the database
    For Each tbl In cat.Tables
        ' Skip system tables
        If Left(tbl.Name, 4) <> "MSys" Then
            ' Set the SQL query to select all data from the current table
            strSQL = "SELECT * FROM [" & tbl.Name & "]"
            
            ' Create a recordset based on the SQL query
            Set rs = CreateObject("ADODB.Recordset")
            rs.Open strSQL, conn
            
            ' Export data to a CSV file
            Open csvFolderPath & tbl.Name & ".csv" For Output As #1
            ' Write header row
            For i = 1 To rs.Fields.Count
                If i <> rs.Fields.Count Then
                    Print #1, rs.Fields(i - 1).Name & ",";
                Else
                    Print #1, rs.Fields(i - 1).Name
                End If
            Next i
            ' Write data rows
            Do Until rs.EOF
                For i = 1 To rs.Fields.Count
                    If i <> rs.Fields.Count Then
                        Print #1, rs.Fields(i - 1) & ",";
                    Else
                        Print #1, rs.Fields(i - 1)
                    End If
                Next i
                rs.MoveNext
            Loop
            Close #1
            
            ' Close the recordset
            rs.Close
            Set rs = Nothing
        End If
    Next tbl
    
    ' Close the connection
    conn.Close
    Set cat = Nothing
    Set conn = Nothing
    
    MsgBox "All tables have been exported to CSV files in " & csvFolderPath
End Sub
