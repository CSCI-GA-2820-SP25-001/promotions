$(function () {
    console.log("[Debug] ✅ rest_api.js fully loaded");

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promotion_db_id").val(res.id);
        $("#promotion_id").val(res.promotion_id);                    // HTML ID: promotion_id
        $("#promotion_name").val(res.name);                          // HTML ID: promotion_name
        $("#start_date").val(res.start_date.slice(0, 10));           // HTML ID: start_date
        $("#end_date").val(res.end_date.slice(0, 10));               // HTML ID: end_date
        $("#type").val(res.promotion_type);                          // HTML ID: type
        $("#amount").val(res.promotion_amount);                      // HTML ID: amount
        $("#description").val(res.promotion_description);            // HTML ID: description
        $("#usage").val(res.usage_count);                            // HTML ID: usage
        $("#state").val(res.state);                                  // HTML ID: state
    }
    

    /// Clears all form fields
    function clear_form_data() {
        $("#promotion_db_id").val("");
        $("#promotion_id").val("");
        $("#promotion_name").val("");
        $("#start_date").val("");
        $("#end_date").val("");
        $("#type").val("");
        $("#amount").val("");
        $("#description").val("");
        $("#usage").val("");
        $("#state").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function (event) {
        event.preventDefault();
        let name = $("#promotion_name").val();
        let promotion_id = $("#promotion_id").val();
        let start_date = $("#start_date").val();
        let end_date = $("#end_date").val();
        let promotion_type = $("#type").val();
        let promotion_amount = parseInt($("#amount").val()) || 0;
        let promotion_description = $("#description").val();
        let usage_count = parseInt($("#usage").val()) || 0;
        let state = $("#state").val();

        let data = {
            // "id": id,
            "name": name,
            "promotion_id": promotion_id,
            "start_date": start_date,
            "end_date": end_date,
            "promotion_type": promotion_type,
            "promotion_amount": promotion_amount,
            "promotion_description": promotion_description,
            "usage_count": usage_count,
            "state": state
        };
        console.log("[Debug] Data before send:", data)

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            console.log("[Debug] AJAX response:", res);
            $("#id_clipboard").val(res.id); 
            console.log("[Debug] Saved to hidden field:", $("#id_clipboard").val());

            update_form_data(res)
            flash_message("Promotion created successfully")
        });

        ajax.fail(function(res){
            console.log("[Debug] Create failed", res);
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {

        let id = $("#promotion_db_id").val();
        let name = $("#promotion_name").val();
        let promotion_id = $("#promotion_id").val();
        let start_date = $("#start_date").val();
        let end_date = $("#end_date").val();
        let promotion_type = $("#type").val();
        let promotion_amount = $("#amount").val();
        let promotion_description = $("#description").val();
        let usage_count = parseInt($("#usage").val()) || 0;
        let state = $("#state").val();

        let data = {
            "id": id,
            "name": name,
            "promotion_id": promotion_id,
            "start_date": start_date,
            "end_date": end_date,
            "promotion_type": promotion_type,
            "promotion_amount": promotion_amount,
            "promotion_description": promotion_description,
            "usage_count": usage_count,
            "state": state
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/promotions/${id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Promotion updated successfully")

        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {
        let id = $("#promotion_db_id").val();
    
        $("#flash_message").empty();
    
        let ajax = $.ajax({
            type: "GET",
            url: `/promotions/${id}`, 
            contentType: "application/json"
        });
    
        ajax.done(function(res){
            console.log("[Retrieve] AJAX response:", res);
            update_form_data(res);
    
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th>promotion_db_id</th>'
            table += '<th>promotion_id</th>'
            table += '<th>name</th>'
            table += '<th>start_date</th>'
            table += '<th>end_date</th>'
            table += '<th>promotion_type</th>'
            table += '<th>promotion_amount</th>'
            table += '<th>promotion_description</th>'
            table += '<th>usage_count</th>'
            table += '<th>state</th>'
            table += '</tr></thead><tbody>'
    
            table +=  `<tr><td>${res.id}</td><td>${res.promotion_id}</td><td>${res.name}</td><td>${res.start_date}</td><td>${res.end_date}</td><td>${res.promotion_type}</td><td>${res.promotion_amount}</td><td>${res.promotion_description}</td><td>${res.usage_count}</td><td>${res.state}</td></tr>`
    
            table += '</tbody></table>';
            $("#search_results").append(table);
            flash_message("Promotion retrieved successfully");
        });
    
        ajax.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
        });
    });
    

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {

        let id = $("#promotion_db_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/promotions/${id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#promotion_db_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Promotion
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#promotion_name").val();
        let category = $("#promotion_category").val();
        let available = $("#promotion_available").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">promotion_db_id</th>'
            table += '<th class="col-md-2">promotion_id</th>'
            table += '<th class="col-md-2">name</th>'
            table += '<th class="col-md-2">start_date</th>'
            table += '<th class="col-md-2">end_date</th>'
            table += '<th class="col-md-2">promotion_type</th>'
            table += '<th class="col-md-2">promotion_amount</th>'
            table += '<th class="col-md-2">promotion_description</th>'
            table += '<th class="col-md-2">usage_count</th>'
            table += '<th class="col-md-2">state</th>'
            table += '</tr></thead><tbody>'
            let firstPromotion = "";
            for(let i = 0; i < res.length; i++) {
                let promotion = res[i];
                table +=  `<tr id="row_${i}"><td>${promotion.id}</td><td>${promotion.promotion_id}</td><td>${promotion.name}</td><td>${promotion.start_date}</td><td>${promotion.end_date}</td><td>${promotion.promotion_type}</td><td>${promotion.promotion_amount}</td><td>${promotion.promotion_description}</td><td>${promotion.usage_count}</td><td>${promotion.state}</td></tr>`;
                if (i == 0) {
                    firstPromotion = promotion;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstPromotion != "") {
                update_form_data(firstPromotion)
            }

            flash_message("Promotion found!!!");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
