$(function () {
    $("div[data-toggle=fieldset]").each(function () {
        const $this = $(this);
        //Add new entry
        $this.find("button[data-toggle=fieldset-add-row]").click(function () {
            let target = $($(this).data("target"));
            // console.log(target);
            let old_row = target.find("[data-toggle=fieldset-entry]:last");
            let row = old_row.clone(true, true);
            let elem_id = row.find(":input")[0].id;
            let elem_prefix = elem_id.replace(/(.*)-(\d{1,4})/m, '$1')// max 4 digits for ids in list
            let elem_num = parseInt(elem_id.replace(/(.*)-(\d{1,4})/m, '$2')) + 1;
            //console.log(elem_prefix);
            //console.log(elem_num);
            row.children(':input').each(function () {
                let id = $(this).attr('id').replace(elem_prefix + '-' + (elem_num - 1), elem_prefix + '-' + (elem_num));
                $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
            });
            row.children('label').each(function () {
                let id = $(this).attr('for').replace(elem_prefix + '-' + (elem_num - 1), elem_prefix + '-' + (elem_num));
                $(this).attr('for', id);
            });
            row.show();
            old_row.after(row);
        }); //End add new entry
        //Remove row
        $this.find("button[data-toggle=fieldset-remove-row]").click(function () {
            if ($this.find("[data-toggle=fieldset-entry]").length > 1) {
                let thisRow = $(this).closest("[data-toggle=fieldset-entry]");
                thisRow.remove();
            }
        }); //End remove row
    });
})
