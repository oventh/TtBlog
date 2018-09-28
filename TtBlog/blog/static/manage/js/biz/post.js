var vm = avalon.define({
    $id: 'post',

    id: '',
    title: '',
    summary: '',
    content: '',
    categories: [],
    tags: [],
    csrfmiddlewaretoken: '',
    defaultChecked: false,

    selectedCategories: [],
    selectedTags: [],

    getCategories: function () {

        $.getJSON('/api/getcategories', {}, function (result) {
            vm.categories = result;
        })

    },

    getTags: function () {

        $.getJSON('/api/gettags', {}, function (result) {
            vm.tags = result;
        })
    },

    checkedCategory: function (e) {
        if (e.target.checked)
            vm.selectedCategories.push(e.target.value);
        else {
            for (let i = 0; i < vm.selectedCategories.length; i++) {
                if (vm.selectedCategories[i] == e.target.value) {
                    vm.selectedCategories.removeAt(i);
                    break;
                }
            }
        }
    },

    checkedTag: function (e) {
        if (e.target.checked)
            vm.selectedTags.push(e.target.value);
        else {
            for (let i = 0; i < vm.selectedTags.length; i++) {
                if (vm.selectedTags[i] == e.target.value) {
                    vm.selectedTags.removeAt(i);
                    break;
                }
            }
        }
    },

    save: function () {
        $.post("/api/savepost", {
            title: vm.title,
            content: editor.txt.html(),
            summary: vm.summary,
            category: JSON.stringify(vm.selectedCategories),
            tag: JSON.stringify(vm.selectedTags),
            csrfmiddlewaretoken: vm.csrfmiddlewaretoken
        }, function (result) {
            if (result.result == true) {

                layer.confirm('文章保存已成功！', {
                    btn: ['继续添加', '返回'] //按钮
                }, function () {
                    window.location.href = "/manage/addpost";
                }, function () {
                    window.location.href = "/manage/content";
                });
            } else {
                layer.alert("保存文章时发生错误，原因：{0}".format(result.err))
            }
        }, "JSON");
    },

    remove: function (id) {
        if(id == '')
            return;

        $.getJSON('/api/removepost',{
            id: id,
            stamp: Date().toLocaleString()
        }, function (res) {
            if(res.result)
                layer.alert("删除文章已成功！");
            else
                layer.alert("删除文章失败，原因：", res.err);
        })
    },
})