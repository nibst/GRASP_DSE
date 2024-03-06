; ModuleID = 'a.g.ld.5.gdce.bc'
source_filename = "llvm-link"
target datalayout = "e-m:e-i64:64-i128:128-i256:256-i512:512-i1024:1024-i2048:2048-i4096:4096-n8:16:32:64-S128-v16:16-v24:32-v32:32-v48:64-v96:128-v192:256-v256:256-v512:512-v1024:1024"
target triple = "fpga64-xilinx-none"

@llvm.global_ctors = appending global [0 x { i32, void ()*, i8* }] zeroinitializer

; Function Attrs: nounwind
define void @_Z7examplePiS_(i32* "fpga.decayed.dim.hint"="8000" %a, i32* "fpga.decayed.dim.hint"="8000" %b) #0 !dbg !253 !fpga.function.pragma !258 {
entry:
  %a.addr = alloca i32*, align 8
  %b.addr = alloca i32*, align 8
  %buff = alloca [8000 x i32], align 4
  %i = alloca i32, align 4
  store i32* %a, i32** %a.addr, align 8
  call void @llvm.dbg.declare(metadata i32** %a.addr, metadata !261, metadata !DIExpression()), !dbg !262
  store i32* %b, i32** %b.addr, align 8
  call void @llvm.dbg.declare(metadata i32** %b.addr, metadata !263, metadata !DIExpression()), !dbg !264
  %0 = bitcast [8000 x i32]* %buff to i8*, !dbg !265
  call void @llvm.lifetime.start.p0i8(i64 32000, i8* %0) #3, !dbg !265
  call void @llvm.dbg.declare(metadata [8000 x i32]* %buff, metadata !266, metadata !DIExpression()), !dbg !270
  br label %example_label0, !dbg !265

example_label0:                                   ; preds = %entry
  %1 = bitcast i32* %i to i8*, !dbg !271
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %1) #3, !dbg !271
  call void @llvm.dbg.declare(metadata i32* %i, metadata !273, metadata !DIExpression()), !dbg !274
  store i32 0, i32* %i, align 4, !dbg !274
  br label %for.cond, !dbg !271

for.cond:                                         ; preds = %for.inc, %example_label0
  %2 = load i32, i32* %i, align 4, !dbg !275
  %cmp = icmp slt i32 %2, 8000, !dbg !277
  br i1 %cmp, label %for.body, label %for.cond.cleanup, !dbg !278

for.cond.cleanup:                                 ; preds = %for.cond
  %3 = bitcast i32* %i to i8*, !dbg !279
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %3) #3, !dbg !279
  br label %for.end

for.body:                                         ; preds = %for.cond
  %4 = load i32*, i32** %a.addr, align 8, !dbg !280
  %5 = load i32, i32* %i, align 4, !dbg !282
  %idxprom = sext i32 %5 to i64, !dbg !280
  %arrayidx = getelementptr inbounds i32, i32* %4, i64 %idxprom, !dbg !280
  %6 = load i32, i32* %arrayidx, align 4, !dbg !280
  %7 = load i32, i32* %i, align 4, !dbg !283
  %idxprom1 = sext i32 %7 to i64, !dbg !284
  %arrayidx2 = getelementptr inbounds [8000 x i32], [8000 x i32]* %buff, i64 0, i64 %idxprom1, !dbg !284
  store i32 %6, i32* %arrayidx2, align 4, !dbg !285
  %8 = load i32, i32* %i, align 4, !dbg !286
  %idxprom3 = sext i32 %8 to i64, !dbg !287
  %arrayidx4 = getelementptr inbounds [8000 x i32], [8000 x i32]* %buff, i64 0, i64 %idxprom3, !dbg !287
  %9 = load i32, i32* %arrayidx4, align 4, !dbg !287
  %add = add nsw i32 %9, 100, !dbg !288
  %10 = load i32, i32* %i, align 4, !dbg !289
  %idxprom5 = sext i32 %10 to i64, !dbg !290
  %arrayidx6 = getelementptr inbounds [8000 x i32], [8000 x i32]* %buff, i64 0, i64 %idxprom5, !dbg !290
  store i32 %add, i32* %arrayidx6, align 4, !dbg !291
  %11 = load i32, i32* %i, align 4, !dbg !292
  %idxprom7 = sext i32 %11 to i64, !dbg !293
  %arrayidx8 = getelementptr inbounds [8000 x i32], [8000 x i32]* %buff, i64 0, i64 %idxprom7, !dbg !293
  %12 = load i32, i32* %arrayidx8, align 4, !dbg !293
  %13 = load i32*, i32** %b.addr, align 8, !dbg !294
  %14 = load i32, i32* %i, align 4, !dbg !295
  %idxprom9 = sext i32 %14 to i64, !dbg !294
  %arrayidx10 = getelementptr inbounds i32, i32* %13, i64 %idxprom9, !dbg !294
  store i32 %12, i32* %arrayidx10, align 4, !dbg !296
  br label %for.inc, !dbg !297

for.inc:                                          ; preds = %for.body
  %15 = load i32, i32* %i, align 4, !dbg !298
  %inc = add nsw i32 %15, 1, !dbg !298
  store i32 %inc, i32* %i, align 4, !dbg !298
  br label %for.cond, !dbg !279, !llvm.loop !299

for.end:                                          ; preds = %for.cond.cleanup
  %16 = bitcast [8000 x i32]* %buff to i8*, !dbg !302
  call void @llvm.lifetime.end.p0i8(i64 32000, i8* %16) #3, !dbg !302
  ret void, !dbg !302
}

; Function Attrs: noinline norecurse optnone uwtable
define i32 @main(i32 %argc, i8** %argv) #4 {
entry:
  %retval = alloca i32, align 4
  %argc.addr = alloca i32, align 4
  %argv.addr = alloca i8**, align 8
  %indata = alloca [8000 x i32], align 16
  %outdata = alloca [8000 x i32], align 16
  store i32 0, i32* %retval, align 4
  store i32 %argc, i32* %argc.addr, align 4
  store i8** %argv, i8*** %argv.addr, align 8
  %arraydecay = getelementptr inbounds [8000 x i32], [8000 x i32]* %indata, i32 0, i32 0
  %0 = load i8**, i8*** %argv.addr, align 8
  %arrayidx = getelementptr inbounds i8*, i8** %0, i64 1
  %1 = load i8*, i8** %arrayidx, align 8
  call void @populateInput(i32* %arraydecay, i32 8000, i8* %1)
  %arraydecay1 = getelementptr inbounds [8000 x i32], [8000 x i32]* %indata, i32 0, i32 0
  %arraydecay2 = getelementptr inbounds [8000 x i32], [8000 x i32]* %outdata, i32 0, i32 0
  call void @_Z7examplePiS_(i32* %arraydecay1, i32* %arraydecay2)
  %arraydecay3 = getelementptr inbounds [8000 x i32], [8000 x i32]* %outdata, i32 0, i32 0
  %2 = load i8**, i8*** %argv.addr, align 8
  %arrayidx4 = getelementptr inbounds i8*, i8** %2, i64 2
  %3 = load i8*, i8** %arrayidx4, align 8
  call void @populateOutput(i32* %arraydecay3, i32 8000, i8* %3)
  ret i32 0
}
declare void @populateInput(i32*, i32, i8*) #5

declare void @populateOutput(i32*, i32, i8*) #5

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: argmemonly nounwind
declare void @llvm.lifetime.start.p0i8(i64, i8* nocapture) #2

; Function Attrs: argmemonly nounwind
declare void @llvm.lifetime.end.p0i8(i64, i8* nocapture) #2

attributes #0 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "fpga.demangled.name"="example" "fpga.top.func"="example" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { argmemonly nounwind }
attributes #3 = { nounwind }
attributes #4 = { noinline norecurse optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
!llvm.dbg.cu = !{!0}
!llvm.ident = !{!249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249, !249}
!llvm.module.flags = !{!250, !251, !252}

!0 = distinct !DICompileUnit(language: DW_LANG_C_plus_plus, file: !1, producer: "clang version 7.0.0 ", isOptimized: true, runtimeVersion: 0, emissionKind: FullDebug, enums: !2, imports: !3)
!1 = !DIFile(filename: "/home/nikolas/Documents/IC_Things/hls-llvm-examples/override_opt_flow_demo/synthesis_input/solution1/.autopilot/db/synthesizable_input.pp.0.cpp", directory: "/home/nikolas/Documents/IC_Things/hls-llvm-examples/override_opt_flow_demo")
!2 = !{}
!3 = !{!4, !12, !16, !23, !27, !32, !34, !42, !46, !50, !64, !68, !72, !76, !80, !85, !89, !93, !97, !101, !109, !113, !117, !119, !123, !127, !132, !138, !142, !146, !148, !156, !160, !168, !170, !174, !178, !182, !186, !191, !196, !201, !202, !203, !204, !206, !207, !208, !209, !210, !211, !212, !214, !215, !216, !217, !218, !219, !220, !225, !226, !227, !228, !229, !230, !231, !232, !233, !234, !235, !236, !237, !238, !239, !240, !241, !242, !243, !244, !245, !246, !247, !248}
!4 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !6, file: !11, line: 52)
!5 = !DINamespace(name: "std", scope: null)
!6 = !DISubprogram(name: "abs", scope: !7, file: !7, line: 848, type: !8, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!7 = !DIFile(filename: "/usr/include/stdlib.h", directory: "/home/nikolas/Documents/IC_Things/hls-llvm-examples/override_opt_flow_demo")
!8 = !DISubroutineType(types: !9)
!9 = !{!10, !10}
!10 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!11 = !DIFile(filename: "/tools/Xilinx/Vitis_HLS/2023.1/tps/lnx64/gcc-8.3.0/lib/gcc/x86_64-pc-linux-gnu/8.3.0/../../../../include/c++/8.3.0/bits/std_abs.h", directory: "/home/nikolas/Documents/IC_Things/hls-llvm-examples/override_opt_flow_demo")
!12 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !13, file: !15, line: 127)
!13 = !DIDerivedType(tag: DW_TAG_typedef, name: "div_t", file: !7, line: 63, baseType: !14)
!14 = distinct !DICompositeType(tag: DW_TAG_structure_type, file: !7, line: 59, size: 64, align: 32, flags: DIFlagFwdDecl, identifier: "_ZTS5div_t")
!15 = !DIFile(filename: "/tools/Xilinx/Vitis_HLS/2023.1/tps/lnx64/gcc-8.3.0/lib/gcc/x86_64-pc-linux-gnu/8.3.0/../../../../include/c++/8.3.0/cstdlib", directory: "/home/nikolas/Documents/IC_Things/hls-llvm-examples/override_opt_flow_demo")
!16 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !17, file: !15, line: 128)
!17 = !DIDerivedType(tag: DW_TAG_typedef, name: "ldiv_t", file: !7, line: 71, baseType: !18)
!18 = distinct !DICompositeType(tag: DW_TAG_structure_type, file: !7, line: 67, size: 128, flags: DIFlagTypePassByValue, elements: !19, identifier: "_ZTS6ldiv_t")
!19 = !{!20, !22}
!20 = !DIDerivedType(tag: DW_TAG_member, name: "quot", scope: !18, file: !7, line: 69, baseType: !21, size: 64)
!21 = !DIBasicType(name: "long int", size: 64, encoding: DW_ATE_signed)
!22 = !DIDerivedType(tag: DW_TAG_member, name: "rem", scope: !18, file: !7, line: 70, baseType: !21, size: 64, offset: 64)
!23 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !24, file: !15, line: 130)
!24 = !DISubprogram(name: "abort", scope: !7, file: !7, line: 598, type: !25, isLocal: false, isDefinition: false, flags: DIFlagPrototyped | DIFlagNoReturn, isOptimized: false)
!25 = !DISubroutineType(types: !26)
!26 = !{null}
!27 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !28, file: !15, line: 134)
!28 = !DISubprogram(name: "atexit", scope: !7, file: !7, line: 602, type: !29, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!29 = !DISubroutineType(types: !30)
!30 = !{!10, !31}
!31 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !25, size: 64)
!32 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !33, file: !15, line: 137)
!33 = !DISubprogram(name: "at_quick_exit", scope: !7, file: !7, line: 607, type: !29, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!34 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !35, file: !15, line: 140)
!35 = !DISubprogram(name: "atof", scope: !7, file: !7, line: 102, type: !36, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!36 = !DISubroutineType(types: !37)
!37 = !{!38, !39}
!38 = !DIBasicType(name: "double", size: 64, encoding: DW_ATE_float)
!39 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !40, size: 64)
!40 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !41)
!41 = !DIBasicType(name: "char", size: 8, encoding: DW_ATE_signed_char)
!42 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !43, file: !15, line: 141)
!43 = !DISubprogram(name: "atoi", scope: !7, file: !7, line: 105, type: !44, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!44 = !DISubroutineType(types: !45)
!45 = !{!10, !39}
!46 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !47, file: !15, line: 142)
!47 = !DISubprogram(name: "atol", scope: !7, file: !7, line: 108, type: !48, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!48 = !DISubroutineType(types: !49)
!49 = !{!21, !39}
!50 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !51, file: !15, line: 143)
!51 = !DISubprogram(name: "bsearch", scope: !7, file: !7, line: 828, type: !52, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!52 = !DISubroutineType(types: !53)
!53 = !{!54, !55, !55, !57, !57, !60}
!54 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: null, size: 64)
!55 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !56, size: 64)
!56 = !DIDerivedType(tag: DW_TAG_const_type, baseType: null)
!57 = !DIDerivedType(tag: DW_TAG_typedef, name: "size_t", file: !58, line: 62, baseType: !59)
!58 = !DIFile(filename: "/tools/Xilinx/Vitis_HLS/2023.1/lnx64/tools/clang-3.9-csynth/lib/clang/7.0.0/include/stddef.h", directory: "/home/nikolas/Documents/IC_Things/hls-llvm-examples/override_opt_flow_demo")
!59 = !DIBasicType(name: "long unsigned int", size: 64, encoding: DW_ATE_unsigned)
!60 = !DIDerivedType(tag: DW_TAG_typedef, name: "__compar_fn_t", file: !7, line: 816, baseType: !61)
!61 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !62, size: 64)
!62 = !DISubroutineType(types: !63)
!63 = !{!10, !55, !55}
!64 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !65, file: !15, line: 144)
!65 = !DISubprogram(name: "calloc", scope: !7, file: !7, line: 543, type: !66, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!66 = !DISubroutineType(types: !67)
!67 = !{!54, !57, !57}
!68 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !69, file: !15, line: 145)
!69 = !DISubprogram(name: "div", scope: !7, file: !7, line: 860, type: !70, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!70 = !DISubroutineType(types: !71)
!71 = !{!13, !10, !10}
!72 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !73, file: !15, line: 146)
!73 = !DISubprogram(name: "exit", scope: !7, file: !7, line: 624, type: !74, isLocal: false, isDefinition: false, flags: DIFlagPrototyped | DIFlagNoReturn, isOptimized: false)
!74 = !DISubroutineType(types: !75)
!75 = !{null, !10}
!76 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !77, file: !15, line: 147)
!77 = !DISubprogram(name: "free", scope: !7, file: !7, line: 555, type: !78, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!78 = !DISubroutineType(types: !79)
!79 = !{null, !54}
!80 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !81, file: !15, line: 148)
!81 = !DISubprogram(name: "getenv", scope: !7, file: !7, line: 641, type: !82, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!82 = !DISubroutineType(types: !83)
!83 = !{!84, !39}
!84 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !41, size: 64)
!85 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !86, file: !15, line: 149)
!86 = !DISubprogram(name: "labs", scope: !7, file: !7, line: 849, type: !87, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!87 = !DISubroutineType(types: !88)
!88 = !{!21, !21}
!89 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !90, file: !15, line: 150)
!90 = !DISubprogram(name: "ldiv", scope: !7, file: !7, line: 862, type: !91, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!91 = !DISubroutineType(types: !92)
!92 = !{!17, !21, !21}
!93 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !94, file: !15, line: 151)
!94 = !DISubprogram(name: "malloc", scope: !7, file: !7, line: 540, type: !95, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!95 = !DISubroutineType(types: !96)
!96 = !{!54, !57}
!97 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !98, file: !15, line: 153)
!98 = !DISubprogram(name: "mblen", scope: !7, file: !7, line: 930, type: !99, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!99 = !DISubroutineType(types: !100)
!100 = !{!10, !39, !57}
!101 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !102, file: !15, line: 154)
!102 = !DISubprogram(name: "mbstowcs", scope: !7, file: !7, line: 941, type: !103, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!103 = !DISubroutineType(types: !104)
!104 = !{!57, !105, !108, !57}
!105 = !DIDerivedType(tag: DW_TAG_restrict_type, baseType: !106)
!106 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !107, size: 64)
!107 = !DIBasicType(name: "wchar_t", size: 32, encoding: DW_ATE_signed)
!108 = !DIDerivedType(tag: DW_TAG_restrict_type, baseType: !39)
!109 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !110, file: !15, line: 155)
!110 = !DISubprogram(name: "mbtowc", scope: !7, file: !7, line: 933, type: !111, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!111 = !DISubroutineType(types: !112)
!112 = !{!10, !105, !108, !57}
!113 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !114, file: !15, line: 157)
!114 = !DISubprogram(name: "qsort", scope: !7, file: !7, line: 838, type: !115, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!115 = !DISubroutineType(types: !116)
!116 = !{null, !54, !57, !57, !60}
!117 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !118, file: !15, line: 160)
!118 = !DISubprogram(name: "quick_exit", scope: !7, file: !7, line: 630, type: !74, isLocal: false, isDefinition: false, flags: DIFlagPrototyped | DIFlagNoReturn, isOptimized: false)
!119 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !120, file: !15, line: 163)
!120 = !DISubprogram(name: "rand", scope: !7, file: !7, line: 454, type: !121, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!121 = !DISubroutineType(types: !122)
!122 = !{!10}
!123 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !124, file: !15, line: 164)
!124 = !DISubprogram(name: "realloc", scope: !7, file: !7, line: 551, type: !125, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!125 = !DISubroutineType(types: !126)
!126 = !{!54, !54, !57}
!127 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !128, file: !15, line: 165)
!128 = !DISubprogram(name: "srand", scope: !7, file: !7, line: 456, type: !129, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!129 = !DISubroutineType(types: !130)
!130 = !{null, !131}
!131 = !DIBasicType(name: "unsigned int", size: 32, encoding: DW_ATE_unsigned)
!132 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !133, file: !15, line: 166)
!133 = !DISubprogram(name: "strtod", scope: !7, file: !7, line: 118, type: !134, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!134 = !DISubroutineType(types: !135)
!135 = !{!38, !108, !136}
!136 = !DIDerivedType(tag: DW_TAG_restrict_type, baseType: !137)
!137 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !84, size: 64)
!138 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !139, file: !15, line: 167)
!139 = !DISubprogram(name: "strtol", scope: !7, file: !7, line: 177, type: !140, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!140 = !DISubroutineType(types: !141)
!141 = !{!21, !108, !136, !10}
!142 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !143, file: !15, line: 168)
!143 = !DISubprogram(name: "strtoul", scope: !7, file: !7, line: 181, type: !144, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!144 = !DISubroutineType(types: !145)
!145 = !{!59, !108, !136, !10}
!146 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !147, file: !15, line: 169)
!147 = !DISubprogram(name: "system", scope: !7, file: !7, line: 791, type: !44, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!148 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !149, file: !15, line: 171)
!149 = !DISubprogram(name: "wcstombs", scope: !7, file: !7, line: 945, type: !150, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!150 = !DISubroutineType(types: !151)
!151 = !{!57, !152, !153, !57}
!152 = !DIDerivedType(tag: DW_TAG_restrict_type, baseType: !84)
!153 = !DIDerivedType(tag: DW_TAG_restrict_type, baseType: !154)
!154 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !155, size: 64)
!155 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !107)
!156 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !157, file: !15, line: 172)
!157 = !DISubprogram(name: "wctomb", scope: !7, file: !7, line: 937, type: !158, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!158 = !DISubroutineType(types: !159)
!159 = !{!10, !84, !107}
!160 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !161, entity: !162, file: !15, line: 200)
!161 = !DINamespace(name: "__gnu_cxx", scope: null)
!162 = !DIDerivedType(tag: DW_TAG_typedef, name: "lldiv_t", file: !7, line: 81, baseType: !163)
!163 = distinct !DICompositeType(tag: DW_TAG_structure_type, file: !7, line: 77, size: 128, flags: DIFlagTypePassByValue, elements: !164, identifier: "_ZTS7lldiv_t")
!164 = !{!165, !167}
!165 = !DIDerivedType(tag: DW_TAG_member, name: "quot", scope: !163, file: !7, line: 79, baseType: !166, size: 64)
!166 = !DIBasicType(name: "long long int", size: 64, encoding: DW_ATE_signed)
!167 = !DIDerivedType(tag: DW_TAG_member, name: "rem", scope: !163, file: !7, line: 80, baseType: !166, size: 64, offset: 64)
!168 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !161, entity: !169, file: !15, line: 206)
!169 = !DISubprogram(name: "_Exit", scope: !7, file: !7, line: 636, type: !74, isLocal: false, isDefinition: false, flags: DIFlagPrototyped | DIFlagNoReturn, isOptimized: false)
!170 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !161, entity: !171, file: !15, line: 210)
!171 = !DISubprogram(name: "llabs", scope: !7, file: !7, line: 852, type: !172, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!172 = !DISubroutineType(types: !173)
!173 = !{!166, !166}
!174 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !161, entity: !175, file: !15, line: 216)
!175 = !DISubprogram(name: "lldiv", scope: !7, file: !7, line: 866, type: !176, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!176 = !DISubroutineType(types: !177)
!177 = !{!162, !166, !166}
!178 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !161, entity: !179, file: !15, line: 227)
!179 = !DISubprogram(name: "atoll", scope: !7, file: !7, line: 113, type: !180, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!180 = !DISubroutineType(types: !181)
!181 = !{!166, !39}
!182 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !161, entity: !183, file: !15, line: 228)
!183 = !DISubprogram(name: "strtoll", scope: !7, file: !7, line: 201, type: !184, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!184 = !DISubroutineType(types: !185)
!185 = !{!166, !108, !136, !10}
!186 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !161, entity: !187, file: !15, line: 229)
!187 = !DISubprogram(name: "strtoull", scope: !7, file: !7, line: 206, type: !188, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!188 = !DISubroutineType(types: !189)
!189 = !{!190, !108, !136, !10}
!190 = !DIBasicType(name: "long long unsigned int", size: 64, encoding: DW_ATE_unsigned)
!191 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !161, entity: !192, file: !15, line: 231)
!192 = !DISubprogram(name: "strtof", scope: !7, file: !7, line: 124, type: !193, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!193 = !DISubroutineType(types: !194)
!194 = !{!195, !108, !136}
!195 = !DIBasicType(name: "float", size: 32, encoding: DW_ATE_float)
!196 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !161, entity: !197, file: !15, line: 232)
!197 = !DISubprogram(name: "strtold", scope: !7, file: !7, line: 127, type: !198, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!198 = !DISubroutineType(types: !199)
!199 = !{!200, !108, !136}
!200 = !DIBasicType(name: "long double", size: 64, encoding: DW_ATE_float)
!201 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !162, file: !15, line: 240)
!202 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !169, file: !15, line: 242)
!203 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !171, file: !15, line: 244)
!204 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !205, file: !15, line: 245)
!205 = !DISubprogram(name: "div", linkageName: "_ZN9__gnu_cxx3divExx", scope: !161, file: !15, line: 213, type: !176, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!206 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !175, file: !15, line: 246)
!207 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !179, file: !15, line: 248)
!208 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !192, file: !15, line: 249)
!209 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !183, file: !15, line: 250)
!210 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !187, file: !15, line: 251)
!211 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !5, entity: !197, file: !15, line: 252)
!212 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !24, file: !213, line: 38)
!213 = !DIFile(filename: "/tools/Xilinx/Vitis_HLS/2023.1/tps/lnx64/gcc-8.3.0/lib/gcc/x86_64-pc-linux-gnu/8.3.0/../../../../include/c++/8.3.0/stdlib.h", directory: "/home/nikolas/Documents/IC_Things/hls-llvm-examples/override_opt_flow_demo")
!214 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !28, file: !213, line: 39)
!215 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !73, file: !213, line: 40)
!216 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !33, file: !213, line: 43)
!217 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !118, file: !213, line: 46)
!218 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !13, file: !213, line: 51)
!219 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !17, file: !213, line: 52)
!220 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !221, file: !213, line: 54)
!221 = !DISubprogram(name: "abs", linkageName: "_ZSt3absg", scope: !5, file: !11, line: 102, type: !222, isLocal: false, isDefinition: false, flags: DIFlagPrototyped, isOptimized: false)
!222 = !DISubroutineType(types: !223)
!223 = !{!224, !224}
!224 = !DIBasicType(name: "__float128", size: 128, encoding: DW_ATE_float)
!225 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !35, file: !213, line: 55)
!226 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !43, file: !213, line: 56)
!227 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !47, file: !213, line: 57)
!228 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !51, file: !213, line: 58)
!229 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !65, file: !213, line: 59)
!230 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !205, file: !213, line: 60)
!231 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !77, file: !213, line: 61)
!232 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !81, file: !213, line: 62)
!233 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !86, file: !213, line: 63)
!234 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !90, file: !213, line: 64)
!235 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !94, file: !213, line: 65)
!236 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !98, file: !213, line: 67)
!237 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !102, file: !213, line: 68)
!238 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !110, file: !213, line: 69)
!239 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !114, file: !213, line: 71)
!240 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !120, file: !213, line: 72)
!241 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !124, file: !213, line: 73)
!242 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !128, file: !213, line: 74)
!243 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !133, file: !213, line: 75)
!244 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !139, file: !213, line: 76)
!245 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !143, file: !213, line: 77)
!246 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !147, file: !213, line: 78)
!247 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !149, file: !213, line: 80)
!248 = !DIImportedEntity(tag: DW_TAG_imported_declaration, scope: !0, entity: !157, file: !213, line: 81)
!249 = !{!"clang version 7.0.0 "}
!250 = !{i32 2, !"Dwarf Version", i32 4}
!251 = !{i32 2, !"Debug Info Version", i32 3}
!252 = !{i32 1, !"wchar_size", i32 4}
!253 = distinct !DISubprogram(name: "example", linkageName: "_Z7examplePiS_", scope: !254, file: !254, line: 6, type: !255, isLocal: false, isDefinition: true, scopeLine: 6, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!254 = !DIFile(filename: "synthesizable_input.cpp", directory: "/home/nikolas/Documents/IC_Things/hls-llvm-examples/override_opt_flow_demo")
!255 = !DISubroutineType(types: !256)
!256 = !{null, !257, !257}
!257 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !10, size: 64)
!258 = !{!259}
!259 = !{!"fpga.top", !"user", !260}
!260 = !DILocation(line: 6, column: 16, scope: !253)
!261 = !DILocalVariable(name: "a", arg: 1, scope: !253, file: !254, line: 6, type: !257)
!262 = !DILocation(line: 6, column: 60, scope: !253)
!263 = !DILocalVariable(name: "b", arg: 2, scope: !253, file: !254, line: 6, type: !257)
!264 = !DILocation(line: 6, column: 73, scope: !253)
!265 = !DILocation(line: 8, column: 3, scope: !253)
!266 = !DILocalVariable(name: "buff", scope: !253, file: !254, line: 8, type: !267)
!267 = !DICompositeType(tag: DW_TAG_array_type, baseType: !10, size: 256000, elements: !268)
!268 = !{!269}
!269 = !DISubrange(count: 8000)
!270 = !DILocation(line: 8, column: 7, scope: !253)
!271 = !DILocation(line: 9, column: 23, scope: !272)
!272 = distinct !DILexicalBlock(scope: !253, file: !254, line: 9, column: 18)
!273 = !DILocalVariable(name: "i", scope: !272, file: !254, line: 9, type: !10)
!274 = !DILocation(line: 9, column: 27, scope: !272)
!275 = !DILocation(line: 9, column: 34, scope: !276)
!276 = distinct !DILexicalBlock(scope: !272, file: !254, line: 9, column: 18)
!277 = !DILocation(line: 9, column: 36, scope: !276)
!278 = !DILocation(line: 9, column: 18, scope: !272)
!279 = !DILocation(line: 9, column: 18, scope: !276)
!280 = !DILocation(line: 10, column: 15, scope: !281)
!281 = distinct !DILexicalBlock(scope: !276, file: !254, line: 9, column: 49)
!282 = !DILocation(line: 10, column: 17, scope: !281)
!283 = !DILocation(line: 10, column: 10, scope: !281)
!284 = !DILocation(line: 10, column: 5, scope: !281)
!285 = !DILocation(line: 10, column: 13, scope: !281)
!286 = !DILocation(line: 11, column: 20, scope: !281)
!287 = !DILocation(line: 11, column: 15, scope: !281)
!288 = !DILocation(line: 11, column: 23, scope: !281)
!289 = !DILocation(line: 11, column: 10, scope: !281)
!290 = !DILocation(line: 11, column: 5, scope: !281)
!291 = !DILocation(line: 11, column: 13, scope: !281)
!292 = !DILocation(line: 12, column: 17, scope: !281)
!293 = !DILocation(line: 12, column: 12, scope: !281)
!294 = !DILocation(line: 12, column: 5, scope: !281)
!295 = !DILocation(line: 12, column: 7, scope: !281)
!296 = !DILocation(line: 12, column: 10, scope: !281)
!297 = !DILocation(line: 13, column: 3, scope: !281)
!298 = !DILocation(line: 9, column: 44, scope: !276)
!299 = distinct !{!299, !278, !300, !301}
!300 = !DILocation(line: 13, column: 3, scope: !272)
!301 = !{!"llvm.loop.name", !"example_label0"}
!302 = !DILocation(line: 14, column: 1, scope: !253)