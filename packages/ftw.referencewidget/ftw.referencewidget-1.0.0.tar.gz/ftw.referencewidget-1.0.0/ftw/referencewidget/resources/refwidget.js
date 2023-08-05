(function(global, $, Handlebars) {


  $(function() {

    var widget;

    function initRefBrowser(event){
      widget = {};

      widget.button = $(".referencewidget button");
      widget.button.on("click", openOverlay);
      $(window).one("resize", resize);

      widget.name = widget.button.closest(".field").data("fieldname");

      widget.request_data = {};
      widget.widget_url = "";
      widget.field_id = "";
      widget.list_template = "";
      widget.checkbox_template = "";
      widget.request_path = "";
      widget.sel_type = "";
      widget.page = 1;
      widget.term = "";

      $(".selected_items").each(function(index, target){
        widget.list_template = Handlebars.compile($("#listing-template").html());
        widget.checkbox_template = Handlebars.compile($("#checkbox-template").html());
        widget.sel_type = $(target).closest(".referencewidget").data("type");

        var container = $(this);
        var data = $(this).data("select");
        if (data === undefined){
          return;
        }
        data.forEach(function(item){
          item["title"] = item["title"] + " (" + item["path"] + ")";
          item["selectable"] = true;
          item["traversable"] = false;
          item['addclass'] = "";
          item['tag'] = "span";
          item["selected"] = "checked=\"checked\"";
          item["type"] = widget.sel_type;
          item["name"] = widget.name;
          item["checkbox"] = widget.checkbox_template(item);
          $(container).find("ul").append(widget.list_template(item));
        });
      });

    }

    function openOverlay(event){
      event.stopPropagation();
      event.preventDefault();

      $(".refbrowser").remove();
      widget.list_template = Handlebars.compile($("#listing-template").html());
      widget.checkbox_template = Handlebars.compile($("#checkbox-template").html());
      $(".sortable").sortable();

      var target = $(event.currentTarget);
      widget.sel_type = target.closest(".referencewidget").data("type");
      widget.field_id = target.closest(".field").attr("id");
      var translations = target.closest(".referencewidget").data("trans");
      widget.widget_url = target.closest(".referencewidget").data("url") + "/++widget++" + widget.name;
      var refbrowser_template = Handlebars.compile($("#refbrowser-template").html());
      $("body").append(refbrowser_template(translations));
      build_pathbar("");
      get_data("");

      var overlay = (".refbrowser");

      $(overlay).on("click", ".refbrowser .path a", jump_to);
      $(overlay).on("click", ".refbrowser .search button", search);
      $(overlay).on("keypress", ".refbrowser .search input", function(event){
        if(event.which == 13) {
          search(event);
      }});

      $(overlay).on("keydown", function(event){
        if(event.which == 27){
          $(".refbrowser").remove();
        }
      });
      $(overlay).on("change", ".refbrowser .listing input.ref-checkbox", checkbox_flipped);
      $(overlay).on("click", ".refbrowser button.cancel", function(){$(".refbrowser").remove();});
      $(overlay).on("click", ".refbrowser .ref_list_entry", switch_level);
      $(overlay).on("click", ".refbrowser .listing input.ref-checkbox", function(e) {e.stopPropagation();});
      $(overlay).on("click", ".refbrowser .refbrowser_batching a", change_page);

    }

    function search(event){
      event.stopPropagation();
      event.preventDefault();

      var value = $(event.currentTarget.parentNode).find("input:text").val();
      widget.term = value;
      search_results(widget.term);
    }

    function search_results(term, page){
      $.post(widget.widget_url + "/search_for_refs", {"term": term, "page": page}, function(data){
        $(".refbrowser .refbrowser_batching").remove();
        build_list(data);
        widget.request_data = data
        $(".refbrowser .listing").addClass("search_result");
      });

    }

    function build_pathbar(path){
      $.post(widget.widget_url +"/generate_pathbar", {"origin": path}, function(data){
        var hb_template = Handlebars.compile($("#node-template").html());
        var pathbar = "";
        data.forEach(function(item){
          pathbar += hb_template(item);
        });
        $(".path").html(pathbar);
      });

    }

    function switch_level(event){
      event.preventDefault();
      event.stopPropagation();

      var target = $(event.currentTarget);
      var traversable = target.data("traversable");
      if (traversable === false){
        return;
      }

      var path = target.data("path");
      widget.request_path = path;
      build_pathbar(path);
      get_data(path);
    }

    function change_page(event){
      var target = $(event.currentTarget);
      if (target.hasClass("next")){
        widget.page++;
      }
      else if (target.hasClass("previous")){
        widget.page--;
      }
      else{
        widget.page = parseInt(target.text());
      }
      var listing = target.closest('.formcontrols').siblings('.listing');
      if (listing.hasClass("search_result") === true){
        search_results(widget.term, widget.page);
      }
      else{
        get_data(widget.request_path, widget.page);
      }
    }

    function rebuild_listing(data){
      $(".refbrowser .listing ul").empty();
      var list_html = "";
      for (var key in data) {
        if (data.hasOwnProperty(key)) {
          var item = data[key];
          item["selected"] = "";
          item["extras"] = "";
          item["tag"] = "span";
          item["name"] = widget.name;
          var is_selected = $(".referencewidget .selected_items li[data-path=\"" + item["path"] + "\"]");
          if (is_selected.find("input:checked").length > 0) {
            item["selected"] = "checked=\"checked\"";
          }
          item["addclass"] = "";
          if (item["traversable"]){
            item["addclass"] = "traversable";
            item["tag"] = "a";
            item["extras"] = "href='#'";
          }
          if (item["selectable"]){
            item["type"] = widget.sel_type;
            item["checkbox"] = widget.checkbox_template(item);
          }
          list_html += widget.list_template(item);
        }
      }
      $(".listing ul").append(list_html);
    }

    function build_list(data){
      $(".refbrowser .refbrowser_batching").remove();
      var batch_template = Handlebars.compile($("#batch_template").html());
      $(".refbrowser .batchingcontainer").append(batch_template(data));
      $(".refbrowser .batchingcontainer .previous").html("&laquo;");
      $(".refbrowser .batchingcontainer .next").html("&raquo;");
      rebuild_listing(data["items"]);
      var height = $(".refbrowser .pathbar").outerHeight(true);
      $(".refbrowser .listing").css({ top: height + "px" });

    }

    function get_data(path, page){
      if (page === undefined){
        page = 1;
      }
      $.post(widget.widget_url+"/get_reference_data", {"start": path, "page": page}, function(data){
        widget.request_data = data;
        build_list(widget.request_data);
      });
    }

    function jump_to(event){
      event.stopPropagation();
      event.preventDefault();
      var item = $(event.currentTarget);
      var path = $(item).data("path");
      if ($(item).data("clickable")){
        widget.request_path = path;
        build_pathbar(path);
        get_data(path);
      }
    }

    function resize(){
      $(".refbrowser .pathbar").each(function(item){
          var height = $(this).outerHeight(true);
          var listing = $(this).siblings(".listing");
          listing.css({"top": height + "px"});
        });
    }
    function checkbox_flipped(event){
      event.stopPropagation();
      event.preventDefault();

      var checkbox = event.currentTarget;
      if (checkbox.checked === true){
        var node = $(event.currentTarget.parentNode).clone();
        $(node).find("input").attr("name", widget.name);
        var text = $.trim(node.find("span").text());
        text = text + " (" + node.data("path") + ")";
        node.find("span").text(text);
        $("#" + widget.field_id + " .referencewidget .selected_items ul").append(node);
      }
      else {
        var query = "#" + widget.field_id + " .referencewidget .selected_items li[data-path=\"" + $(event.currentTarget.parentNode).data("path") + "\"]";
        $(query).remove();
      }
    }


    // Regular usecase
    $(window).on('load', function(event){
      if ($(".referencewidget button").length !== 0){
        initRefBrowser(event);
      }
    });
    // Overlays
    $(document).on("onLoad", ".overlay", initRefBrowser);

    // Public api
    window.initRefBrowser = initRefBrowser;

  });


})(window, window.jQuery, window.Handlebars);
