$(document).ready(() => {
    //Read Data
    $("#msg").html("Loading Data ...");
    $.ajax({
        url: "http://localhost:3000/get/engineer/data",
        method: "get",
        dataType: "json",
        timeout: "0",
        success: (response) => {
            var html = '';
            $.each(response, (k,v) => {
                html += `
                    <tr>
                        <td>${v.customer}</td>
                        <td>${v.date_start}</td>
                        <td>${v.engineer}</td>
                    </tr>
                `;
            });
            $("#tbody").html(html).promise().done(() => {
                $("#msg").html("");
                $("#myTable").DataTable();
            })
        },
        error: (err) => {
            console.log(err)
        }
    });
    //Add Token
    $("#btnsave").click((e) => {
        e.preventDefault();
        var txt_username = $("#txtusername").val();
        $.ajax({
            url: "http://localhost:3000/add/token?username=" + txt_username,
            method: "POST",
            timeout: 0,
            headers: {
                "Authorization": "Bearer GtzTI7yFj3TZ3K11WPtcNkbAh4hZRcZ3UQAE5pSfEpbpAHkwsv68dgvvSkp2uoU84dilRYzlUuhJUKExGh"
            },
            success: (response) => {
                $("#msg_alert").show();
                $("#msg_alert").addClass("alert-success");
                $("#msg_alert").html(`
                    Username: ${response.username} <br>
                    Token Key: <strong>${response.token}</strong>
                `)
            },
            error: (err) => {
                $("#msg_alert").show();
                $("#msg_alert").addClass("alert-danger");
                $("#msg_alert").html("Error:" + err);
            }
        });
    });
});