Attribute VB_Name = "Module1"
Sub KNN()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Sheet1") ' Thay "Sheet1" bang ten sheet cua ban
    
    Dim lastRow As Long
    lastRow = 5850 ' Hang cuoi cung cua du lieu
    
    Dim newRow As Long
    newRow = 5854 ' Hang chua du lieu moi can du doan
    
    Dim k As Integer
    k = 5 ' So luong hang xom gan nhat
    
    Dim i As Long, j As Long
    Dim distances() As Long ' Su dung kieu Long de luu khoang cach Hamming
    ReDim distances(1 To lastRow - 1)
    
    ' Tinh khoang cach Hamming giua hang moi va cac hang trong tap du lieu
    For i = 2 To lastRow
        distances(i - 1) = 0
        For j = 1 To 30 ' 30 la so luong thuoc tinh (cot A den AD)
            If ws.Cells(newRow, j).Value <> ws.Cells(i, j).Value Then
                distances(i - 1) = distances(i - 1) + 1
            End If
        Next j
    Next i
    
    ' Tim k hang xom gan nhat
    Dim nearestIndices() As Long
    ReDim nearestIndices(1 To k)
    
    For i = 1 To k
        Dim minDist As Long
        minDist = 999999 ' Gia tri lon de tim khoang cach nho nhat
        Dim minIndex As Long
        minIndex = -1
        
        For j = 1 To lastRow - 1
            If distances(j) < minDist Then
                minDist = distances(j)
                minIndex = j
            End If
        Next j
        
        nearestIndices(i) = minIndex + 1 ' +1 vi mang distances bat dau tu 1
        distances(minIndex) = 999999 ' Danh dau da chon
    Next i
    
    ' In ra 5 dong thuoc tinh gan nhat va nhan trong cua so Immediate
    Debug.Print "5 dong thuoc tinh gan nhat va nhan:"
    For i = 1 To k
        Debug.Print "Dong " & nearestIndices(i) & ": "
        For j = 1 To 30 ' In cac thuoc tinh
            Debug.Print ws.Cells(nearestIndices(i), j).Value & ", ";
        Next j
        Debug.Print "Nhan: " & ws.Cells(nearestIndices(i), 31).Value ' In nhan (cot Result)
        Debug.Print "Khoang cach Hamming: " & minDist
        Debug.Print "----------------------------------------"
    Next i
    
    ' Dem so luong ket qua 1 va -1 trong k hang xom gan nhat
    Dim count1 As Integer
    Dim countNeg1 As Integer
    count1 = 0
    countNeg1 = 0
    
    For i = 1 To k
        If ws.Cells(nearestIndices(i), 31).Value = 1 Then ' Cot 31 la cot Result
            count1 = count1 + 1
        ElseIf ws.Cells(nearestIndices(i), 31).Value = -1 Then
            countNeg1 = countNeg1 + 1
        End If
    Next i
    
    ' Du doan ket qua
    If count1 > countNeg1 Then
        ws.Cells(5854, 31).Value = 1 ' Ghi ket qua vao hang 5854, cot Result
        MsgBox "Du doan: Web binh thuong."
    Else
        ws.Cells(5854, 31).Value = -1
        MsgBox "Du doan: Web lua dao!!!"
    End If
    
End Sub
