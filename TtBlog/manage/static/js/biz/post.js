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

    //category
    isEditCategory: false,
    editCategoryId: '',
    editCategoryName: '',


    //tag
    isEditTag: false,
    editTagId: '',
    editTagName: '',


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

    get: function(){

        if(vm.id == '')
            return;

        $.getJSON('/api/getpost', {
            id: vm.id,
            stamp: Date().toLocaleLowerCase()
        }, function (res) {
            if(res.data != null){
                vm.title = res.data.Title;
                vm.summary = res.data.Summary;
                vm.selectedTags = res.data.cids;
                vm.selectedCategories = res.data.tids;
                editor.txt.html(res.data.Content);

                //选中文章相关的分类
                if(res.data.cids != null && res.data.cids.length >0){
                    for(let i=0;i<vm.categories.length;i++){
                        for(let j=0;j<res.data.cids.length;j++){
                            if(vm.categories[i].Id == res.data.cids[j])
                                vm.categories[i].Checked = true;
                        }
                    }
                }

                if(res.data.tids != null && res.data.tids.length >0){
                    for(let i=0;i<vm.tags.length;i++){
                        for(let j=0;j<res.data.tids.length;j++){
                            if(vm.tags[i].Id == res.data.tids[j])
                                vm.tags[i].Checked = true;
                        }
                    }
                }
            }
        })
    },

    save: function () {

        let cids= [], tids= [];

        for(let i=0; i<vm.categories.length; i++){
            if(vm.categories[i].Checked)
                cids.push(vm.categories[i].Id);
        }

        for(let i=0;i<vm.tags.length;i++){
            if(vm.tags[i].Checked)
                tids.push(vm.tags[i].Id);
        }


        $.post("/api/savepost", {
            id: vm.id,
            title: vm.title,
            content: editor.txt.html(),
            summary: vm.summary,
            category: JSON.stringify(cids),
            tag: JSON.stringify(tids),
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
                layer.alert("保存文章时发生错误，原因：" + result.err)
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
    },

    // manage category function

    manageCategory: function () {
        vm.getCategories();
        $("#divCategory").modal();
    },

    addCategory: function () {
        vm.editCategoryId = '';
        vm.editCategoryName = '';
        vm.isEditCategory = true;
    },

    editCategory: function(el){
        if(el == null)
            return;

        vm.editCategoryId = el.Id;
        vm.editCategoryName = el.Name;
        vm.isEditCategory = true;
    },

    cancelCategory: function(){

        vm.isEditCategory = false;
        vm.editCategoryId = '';
        vm.editCategoryName = '';
    },

    removeCategory: function(id){
        if(id== '')
            return;

        $.getJSON('/api/removecategory',{
            id: id,
            stamp: Date().toLocaleString()
        }, function (res) {
            if(res.result){
                layer.alert('已删除分类！')
                vm.isEditCategory = false;
                vm.getCategories();
            } else{
                layer.alert('删除分类失改，原因：'+ res.err);
            }
        })

    },

    saveCategory: function () {
        if(vm.editCategoryName == ''){
            layer.alert('请填写必要的信息！');
            return;
        }

        $.getJSON('/api/savecategory',{
            id: vm.editCategoryId,
            name: vm.editCategoryName
        }, function (res) {
            if(res.result){
                layer.alert('保存分类信息已成功！')

                vm.isEditCategory = false;
                vm.getCategories();
            } else{
                layer.alert('保存分类信息失改，原因：' + res.err);
            }
        })
    },

    //tag functions

    manageTag: function () {
        vm.getTags();
        $("#divTag").modal();
    },

    addTag: function () {
        vm.isEditTag = true;
        vm.editTagId = '';
        vm.editTagName = '';
    },

    editTag: function(el){
        vm.isEditTag = true;
        vm.editTagName = el.Name;
        vm.editTagId = el.Id;
    },

    removeTag: function(id){
        if(id == '')
            return;

        $.getJSON('/api/removetag',{
            id: id,
            stamp: Date().toLocaleString()
        }, function (res) {
            if(res.result){
                layer.alert('删除标签信息已成功！')
                vm.isEditTag = false;
                vm.getTags();
            } else {
                layer.alert('删除标签信息失败，原因：'+ res.err);
            }
        })
    },

    saveTag: function () {
        if(vm.editTagName == ''){
            layer.alert('请填写必要的信息！');
            return;
        }

        $.getJSON('/api/savetag',{
            id: vm.editTagId,
            name: vm.editTagName,
        }, function (res) {
            if(res.result){
                layer.alert('保存标签信息已成功！');
                vm.isEditTag = false;
                vm.getTags();
            } else {
                layer.alert('保存标签信息失败，原因：' + res.err);
            }
        })
    },

    cancelTag: function () {
        vm.isEditTag = false;
        vm.editTagName = '';
        vm.editTagId = '';
    }
})