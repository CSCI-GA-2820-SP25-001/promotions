$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promotion_id").val(res.id);
        $("#promotion_name").val(res.name);
        $("#promotion_promotion_id").val(res.promotion_id);
        $("#promotion_start_date").val(res.start_date);
        $("#promotion_end_date").val(res.end_date);
        $("#promotion_promotion_type").val(res.promotion_type);
        $("#promotion_promotion_amount").val(res.promotion_amount);
        $("#promotion_promotion_description").val(res.promotion_description);
        $("#promotion_usage_count").val(res.usage_count);
        $("#promotion_state").val(res.state);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promotion_id").val("");
        $("#promotion_name").val("");
        $("#promotion_promotion_id").val("");
        $("#promotion_start_date").val("");
        $("#promotion_end_date").val("");
        $("#promotion_promotion_type").val("");
        $("#promotion_promotion_amount").val("");
        $("#promotion_promotion_description").val("");
        $("#promotion_usage_count").val("");
        $("#promotion_state").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function () {

        let id = $("#promotion_id").val();
        let name = $("#promotion_name").val();
        let promotion_id = $("#promotion_promotion_id").val();
        let start_date = $("#promotion_start_date").val();
        let end_date = $("#promotion_end_date").val();
        let promotion_type = $("#promotion_promotion_type").val();
        let promotion_amount = $("#promotion_promotion_amount").val();
        let promotion_description = $("#promotion_promotion_description").val();
        let usage_count = $("#promotion_usage_count").val();
        let state = $("#promotion_state").val();

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
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {

        let id = $("#promotion_id").val();
        let name = $("#promotion_name").val();
        let promotion_id = $("#promotion_promotion_id").val();
        let start_date = $("#promotion_start_date").val();
        let end_date = $("#promotion_end_date").val();
        let promotion_type = $("#promotion_promotion_type").val();
        let promotion_amount = $("#promotion_promotion_amount").val();
        let promotion_description = $("#promotion_promotion_description").val();
        let usage_count = $("#promotion_usage_count").val();
        let state = $("#promotion_state").val();

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
                url: `/promotions/${promotion_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions/${promotion_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/promotions/${promotion_id}`,
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
        $("#promotion_id").val("");
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
            table += '<th class="col-md-2">id</th>'
            table += '<th class="col-md-2">name</th>'
            table += '<th class="col-md-2">promotion_id</th>'
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
                table +=  `<tr id="row_${i}"><td>${promotion.id}</td><td>${promotion.name}</td><td>${promotion.promotion_id}</td><td>${promotion.start_date}</td><td>${promotion.end_date}</td><td>${promotion.promotion_type}</td><td>${promotion.promotion_amount}</td><td>${promotion.promotion_description}</td><td>${promotion.usage_count}</td><td>${promotion.state}</td></tr>`;
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

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
