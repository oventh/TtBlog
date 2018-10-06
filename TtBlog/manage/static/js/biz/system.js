var vm = avalon.define({
    $id: 'system',

    name: '',
    summary: '',
    banner: '',
    pageSize: 15,

    
    getSetting: function () {
        $.getJSON('api/getSetting',{
            stamp: Date().toString()
        }, function (res) {
            if(res.result != null)
                vm.name = res.result.Name;
                vm.summary = res.result.Summary;
                vm.banner = res.result.Banner;
        })
    },

    saveSetting: function () {
        if(vm.name == ''){
            layer.alert("请填写必要的信息！");
            return;
        }

        $.post('api/saveSetting', {
            name: vm.name,
            summary: vm.summary,
            Banner: vm.banner,
            pageSize: vm.pageSize
        }, function (res) {
            if(res.result){
                layer.alert("站点配置已保存！")
            } else{
                layer.alert("保存站点配置失败，原因：" + res.err);
            }

        }, "JSON")
    },


})