var result = "# formart: 1\n" +
    "# compiler: Razor 0.6.3\n" +
    "[res name mapping]\n" +
    "com.meitu.meiyancamera:anim/abc_fade_in abc_fade_in 0x7f010000\n" +
    "com.meitu.meiyancamera:id/fl_anim_root HJ 0x7f0a02b2\n" +
    "com.meitu.meiyancamera:id/sb_beautify_adjust l- 0x7f0a0c5f\n" +
    "com.meitu.meiyancamera:id/sb_beautify_feature_restore l_ 0x7f0a0c60\n" +
    "com.meitu.meiyancamera:id/sb_beautify_smart_filter l$ 0x7f0a0c61\n" +
    "com.meitu.meiyancamera:id/sb_beautify_submodule_seek_bar l( 0x7f0a0c62\n" +
    "com.meitu.meiyancamera:id/sb_beautify_submodule_seek_bar_all_skin l) 0x7f0a0c63\n" +
    "com.meitu.meiyancamera:id/sb_beautify_submodule_seek_bar_one l* 0x7f0a0c64\n" +
    "com.meitu.meiyancamera:id/sb_beautify_submodule_seek_bar_two l+ 0x7f0a0c65\n" +
    "com.meitu.meiyancamera:id/sb_beautify_submodule_top_seek_bar l, 0x7f0a0c66\n" +
    "com.meitu.meiyancamera:id/sb_beauty_effect_panel l= 0x7f0a0c67\n" +
    "com.meitu.meiyancamera:id/sb_blurry l[ 0x7f0a0c68\n" +
    "com.meitu.meiyancamera:id/sb_blurry_density l] 0x7f0a0c69\n" +
    "com.meitu.meiyancamera:id/sb_movie_effect_panel l^ 0x7f0a0c6a\n" +
    "com.meitu.meiyancamera:id/sb_record l` 0x7f0a0c6b\n" +
    "com.meitu.meiyancamera:id/sb_remote_ab_enable l{ 0x7f0a0c6c\n" +
    "com.meitu.meiyancamera:id/sb_selfie_alpha l| 0x7f0a0c6d\n" +
    "com.meitu.meiyancamera:id/sb_selfie_edit_seek_bar l} 0x7f0a0c6e\n" +
    "com.meitu.meiyancamera:id/sb_selfie_level l~ 0x7f0a0c6f\n" +
    "com.meitu.meiyancamera:id/sb_selfie_texture_suit_seek_bar mA 0x7f0a0c70\n" +
    "com.meitu.meiyancamera:id/sb_selfie_tide_theme_seek_bar mB 0x7f0a0c71\n" +
    "com.meitu.meiyancamera:id/sbtn_mock mC 0x7f0a0c72\n";
//
// var result = "\n" +
//     "    com.mt.mtxx.mtxx.R.id.toolBar -> com.mt.mtxx.mtxx.R.id.dj2\n" +
//     "    com.mt.mtxx.mtxx.R.id.toolBarLayout -> com.mt.mtxx.mtxx.R.id.dj3\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_background -> com.mt.mtxx.mtxx.R.id.dj4\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_content -> com.mt.mtxx.mtxx.R.id.dj5\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_edit -> com.mt.mtxx.mtxx.R.id.dj6\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_empty -> com.mt.mtxx.mtxx.R.id.dj7\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_icon -> com.mt.mtxx.mtxx.R.id.dj8\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_icon_layout -> com.mt.mtxx.mtxx.R.id.dj9\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_icon_res -> com.mt.mtxx.mtxx.R.id.dj_\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_layout -> com.mt.mtxx.mtxx.R.id.dja\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_status_bar_top_view -> com.mt.mtxx.mtxx.R.id.djb\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_sub_title -> com.mt.mtxx.mtxx.R.id.djc\n" +
//     "    com.mt.mtxx.mtxx.R.id.tool_title -> com.mt.mtxx.mtxx.R.id.djd";

let reg = new RegExp(".*:id\/.* .* ", 'g');
let mappingList = result.match(reg);
let oriMap = {}
if (mappingList != undefined) {
    console.log(mappingList.length);
    for (let mappingInfo of mappingList) {
        let info = mappingInfo.split(' ');
        let index =  info[0].indexOf('/') + 1;
        // oriMap[info[0].substring(0, index) + info[1]] = info[0].substring(index);
        oriMap[info[1]] = info[0].substring(index);
        // console.log(info[0].substring(0, index));
        // console.log(info[0].substring(index));
        // console.log(info[1]);
    }
} else {
    reg = new RegExp(".*R.id.* -> .*R.id.*", 'g')
    let innerReg =  new RegExp(".*R.id.(.*) -> .*R.id.(.*)");
    mappingList = result.match(reg);
    // console.log(mappingList.length);
    for (let mappingInfo of mappingList) {
        let regList = innerReg.exec(mappingInfo);
        if (regList.length > 2) {
            console.log(regList[1], regList[2]);
            oriMap[regList[2]] = regList[1];
        }
    }
}
console.log(oriMap);