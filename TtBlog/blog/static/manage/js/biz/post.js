var vm = avalon.define({
    $id: 'post',

    // post edit
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

    //post query
    posts: [],
    pageSize: 15,
    pageIndex: 1,
    totalRecord: 0,
    totalPage: 0,

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
        layer.confirm('你确定要删除当前选中的文章吗？', {
            btn: ['确定', '返回']
        }, function () {
            $.getJSON('/api/removepost', {
                id: id,
                stamp: Date().toLocaleString()
            }, function (res) {
                if (res.result)
                    layer.alert("删除文章已成功！");
                else
                    layer.alert("删除文章失败，原因：", res.err);
            })
        }, function () {
            return;
        });
    },

    query: function (page) {

        vm.pageIndex = page;

        $.getJSON('/api/querypost',{
            pageIndex: vm.pageIndex,
            pageSize: vm.pageSize,
            stamp: Date().toLocaleString()
        }, function (res) {
             vm.posts = res.result;
             vm.totalPage = res.totalPage;
             vm.totalRecord = res.total;
        })
    },

    prev: function () {
        vm.pageIndex = vm.pageIndex > 1 ? vm.pageIndex -1 : 1;
        vm.query(vm.pageIndex);
    },

    next: function () {
        vm.pageIndex = vm.pageIndex < vm.totalPage ? vm.pageIndex + 1: vm.totalPage;
        vm.query(vm.pageIndex);
    }
})