// All the JavaScript functions for datatable and other calls are defined here
//Defining the datatable.
jQuery(document).ready(function($){
    var dataTable = $('#myTable').DataTable({
        columns: [                  //Defining table structure. Must align with the database collection structure
            { data: 'emp_id' },
            { data: 'first_name' },
            { data: 'last_name' },
            { data: 'email' },
            { data: 'ph_no' },
            { data: 'home_addr' },
            { data: 'st_addr' },
            { data: 'gender' },
            { data: 'job_type' },
            { data: 'edit'},
            { data: 'delete'},
        ],
        searching: true,
        "autoWidth": false,
        responsive: true,
        fixedHeader: true,
    });
    
    // Debug function to inspect table row data
    function getRowData(row) {
        var rowData = {};
        var cells = $(row).find('td, th');
        
        rowData.emp_id = $(cells[0]).text().trim();
        rowData.first_name = $(cells[1]).text().trim();
        rowData.last_name = $(cells[2]).text().trim();
        rowData.email = $(cells[3]).text().trim();
        rowData.ph_no = $(cells[4]).text().trim();
        rowData.home_addr = $(cells[5]).text().trim();
        rowData.st_addr = $(cells[6]).text().trim();
        rowData.gender = $(cells[7]).text().trim();
        rowData.job_type = $(cells[8]).text().trim();
        
        console.log("Row data extracted:", rowData);
        return rowData;
    }
    
    // Handling the edit function
    $("#myTable").on("click", ".edit-button", function(){
        var row = $(this).closest('tr');
        var rowData = getRowData(row);
        
        console.log("Edit button clicked for employee ID:", rowData.emp_id);
        
        // Clear previous values
        $(".modal-body div span").text("");
        
        // Set the employee ID in the modal header
        $(".emp_id span").text(rowData.emp_id);
        
        // Set the values in the edit fields
        document.getElementById("edit-first_name").value = rowData.first_name;
        document.getElementById("edit-last_name").value = rowData.last_name;
        document.getElementById("edit-ph_no").value = rowData.ph_no;
        document.getElementById("edit-home_addr").value = rowData.home_addr;
        document.getElementById("edit-st_addr").value = rowData.st_addr;
        document.getElementById("edit-gender").value = rowData.gender;
        document.getElementById("edit-job_type").value = rowData.job_type;
        
        // Store the employee ID for later use
        $("#myEditModal").data("emp_id", rowData.emp_id);
        
        // Show the modal
        $("#myEditModal").modal("show");
    });
    
    // Handle the edit submit button
    $('#edit_record_button').on('click', function(){
        var emp_id = $("#myEditModal").data("emp_id");
        var first_name = $('#edit-first_name').val();
        var last_name = $('#edit-last_name').val();
        var email = first_name + '.' + last_name + '@acme.com';
        var ph_no = $('#edit-ph_no').val();
        var home_addr = $('#edit-home_addr').val();
        var st_addr = $('#edit-st_addr').val();
        var gender = $('#edit-gender').val();
        var job_type = $('#edit-job_type').val();
        
        console.log("Submitting edit for employee ID:", emp_id);
        console.log("Edit URL:", "/employee/" + emp_id);
        
        // Fields mentioned below cannot be empty
        if(emp_id != '' && first_name != '' && last_name != '' && ph_no != '' && job_type != '') {
            $("#myEditModal").modal("hide");
            
            var formData = {
                emp_id: emp_id,
                first_name: first_name,
                last_name: last_name,
                email: email,
                ph_no: ph_no,
                home_addr: home_addr,
                st_addr: st_addr,
                gender: gender,
                job_type: job_type
            };
            
            console.log("Edit form data:", formData);
            
            $.ajax({
                url: "/employee/" + emp_id,
                method: "PUT",
                data: formData,
                beforeSend: function(xhr) {
                    console.log("Sending PUT request...");
                },
                success: function(data) {
                    console.log("Edit success response:", data);
                    alert(data);
                    if(data == 'No-data') {
                        alert("Invalid Records!");
                    } else {
                        location.reload();
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Edit error status:", status);
                    console.error("Edit error:", error);
                    console.error("Edit error response:", xhr.responseText);
                    alert("Error updating record: " + error);
                }
            });
        } else {
            alert("All Fields are required");
        }
    });

    // Handling the delete function
    $("#myTable").on("click", ".delete-button", function(){
        var row = $(this).closest('tr');
        var rowData = getRowData(row);
        
        console.log("Delete button clicked for employee ID:", rowData.emp_id);
        
        // Clear previous values
        $("#myDeleteModal .modal-body span").text("");
        
        // Set the values in the delete modal
        $("#myDeleteModal .emp_id span").text(rowData.emp_id);
        $("#myDeleteModal .first_name span").text(rowData.first_name);
        $("#myDeleteModal .last_name span").text(rowData.last_name);
        $("#myDeleteModal .email span").text(rowData.email);
        $("#myDeleteModal .ph_no span").text(rowData.ph_no);
        $("#myDeleteModal .home_addr span").text(rowData.home_addr);
        $("#myDeleteModal .st_addr span").text(rowData.st_addr);
        $("#myDeleteModal .gender span").text(rowData.gender);
        $("#myDeleteModal .job_type span").text(rowData.job_type);
        
        // Store the employee ID for later use
        $("#myDeleteModal").data("emp_id", rowData.emp_id);
        
        // Show the delete modal
        $("#myDeleteModal").modal("show");
    });
    
    // Handle the delete submit button
    $('#delete_record_button').on('click', function(){
        var emp_id = $("#myDeleteModal").data("emp_id");
        
        console.log("Deleting employee ID:", emp_id);
        console.log("Delete URL:", "/employee/" + emp_id);
        
        if(emp_id) {
            $("#myDeleteModal").modal("hide");
            
            $.ajax({
                url: "/employee/" + emp_id,
                method: "DELETE",
                contentType: "application/json",
                beforeSend: function(xhr) {
                    console.log("Sending DELETE request...");
                },
                success: function(data) {
                    console.log("Delete success response:", data);
                    alert(data);
                    if(data == 'No-data') {
                        alert("Invalid Records!");
                    } else {
                        location.reload();
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Delete error status:", status);
                    console.error("Delete error:", error);
                    console.error("Delete error response:", xhr.responseText);
                    alert("Error deleting record: " + error);
                }
            });
        } else {
            alert("Employee ID is required");
        }
    });

    // Adding an employee information to the database
    $('#add_record_button').click(function(){
        var table = $('#myTable').DataTable();
        var last_row = table.row(':last').data();
        var last_emp_id = parseInt(last_row.emp_id);
        var emp_id = last_emp_id + 1;
        
        var first_name = $('#first_name').val();
        var last_name = $('#last_name').val();
        var email = first_name + '.' + last_name + '@acme.com';
        var ph_no = $('#ph_no').val();
        var home_addr = $('#home_addr').val();
        var st_addr = $('#st_addr').val();
        var gender = $('#gender').val();
        var job_type = $('#job_type').val();
        
        if(emp_id != '' && first_name != '' && last_name != '' && ph_no != '' && job_type != '') {
            $.ajax({
                url: "/employee",
                method: "POST",
                data: {
                    emp_id: emp_id,
                    first_name: first_name,
                    last_name: last_name,
                    email: email,
                    ph_no: ph_no,
                    home_addr: home_addr,
                    st_addr: st_addr,
                    gender: gender,
                    job_type: job_type
                },
                success: function(data) {
                    alert(data);
                    if(data == 'No-data') {
                        alert("Invalid Records!");
                    } else {
                        $('#addModal').hide();
                        location.reload();
                    }
                },
                error: function(xhr, status, error) {
                    alert("Error adding record: " + error);
                    console.error("Add error:", xhr.responseText);
                }
            });
        } else {
            alert("All Fields are required");
        }
    });
});
