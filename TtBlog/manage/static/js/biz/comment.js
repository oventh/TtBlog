var vm = avalon.define({
    $id: 'comment',

    comments: [],
    pageIndex: 1,
    pageSize: 15,
    totalPage: 0,
    totalRecord: 0,


    query: function (page) {

        vm.pageIndex = page;

        $.getJSON('/api/querycomment/',{
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


})