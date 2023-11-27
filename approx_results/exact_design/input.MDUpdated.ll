; ModuleID = 'input.MDUpdated.bc'
source_filename = "input.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@test_data = dso_local global [8000 x i32] zeroinitializer, align 16
@result = dso_local global [8000 x i32] zeroinitializer, align 16

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_Z7examplePiS_(i32* %a, i32* %b) #0 {
entry:
  %"1.a.addr" = alloca i32*, align 8, !opID !3, !opSignedness !4
  %"2.b.addr" = alloca i32*, align 8, !opID !5, !opSignedness !4
  %"3.buff" = alloca [8000 x i32], align 16, !opID !6, !opSignedness !4
  %"4.i" = alloca i32, align 4, !opID !7, !opSignedness !4
  store i32* %a, i32** %"1.a.addr", align 8, !opID !8, !opSignedness !4
  store i32* %b, i32** %"2.b.addr", align 8, !opID !9, !opSignedness !4
  br label %example_label0, !opID !10, !opSignedness !4

example_label0:                                   ; preds = %entry
  store i32 0, i32* %"4.i", align 4, !opID !11, !opSignedness !4
  br label %for.cond, !opID !12, !opSignedness !4

for.cond:                                         ; preds = %for.inc, %example_label0
  %"10." = load i32, i32* %"4.i", align 4, !opID !13, !opSignedness !4
  %"11.cmp" = icmp slt i32 %"10.", 8000, !opID !14, !opSignedness !4
  br i1 %"11.cmp", label %for.body, label %for.end, !opID !15, !opSignedness !4

for.body:                                         ; preds = %for.cond
  %"13." = load i32*, i32** %"1.a.addr", align 8, !opID !16, !opSignedness !4
  %"14." = load i32, i32* %"4.i", align 4, !opID !17, !opSignedness !4
  %"15.idxprom" = sext i32 %"14." to i64, !opID !18, !opSignedness !4
  %"16.arrayidx" = getelementptr inbounds i32, i32* %"13.", i64 %"15.idxprom", !opID !19, !opSignedness !4
  %"17." = load i32, i32* %"16.arrayidx", align 4, !opID !20, !opSignedness !4
  %"18." = load i32, i32* %"4.i", align 4, !opID !21, !opSignedness !4
  %"19.idxprom1" = sext i32 %"18." to i64, !opID !22, !opSignedness !4
  %"20.arrayidx2" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"3.buff", i64 0, i64 %"19.idxprom1", !opID !23, !opSignedness !4
  store i32 %"17.", i32* %"20.arrayidx2", align 4, !opID !24, !opSignedness !4
  %"22." = load i32, i32* %"4.i", align 4, !opID !25, !opSignedness !4
  %"23.idxprom3" = sext i32 %"22." to i64, !opID !26, !opSignedness !4
  %"24.arrayidx4" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"3.buff", i64 0, i64 %"23.idxprom3", !opID !27, !opSignedness !4
  %"25." = load i32, i32* %"24.arrayidx4", align 4, !opID !28, !opSignedness !4
  %"26.add" = add nsw i32 %"25.", 100, !opID !29, !opSignedness !4
  %"27." = load i32, i32* %"4.i", align 4, !opID !30, !opSignedness !4
  %"28.idxprom5" = sext i32 %"27." to i64, !opID !31, !opSignedness !4
  %"29.arrayidx6" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"3.buff", i64 0, i64 %"28.idxprom5", !opID !32, !opSignedness !4
  store i32 %"26.add", i32* %"29.arrayidx6", align 4, !opID !33, !opSignedness !4
  %"31." = load i32, i32* %"4.i", align 4, !opID !34, !opSignedness !4
  %"32.idxprom7" = sext i32 %"31." to i64, !opID !35, !opSignedness !4
  %"33.arrayidx8" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"3.buff", i64 0, i64 %"32.idxprom7", !opID !36, !opSignedness !4
  %"34." = load i32, i32* %"33.arrayidx8", align 4, !opID !37, !opSignedness !4
  %"35." = load i32*, i32** %"2.b.addr", align 8, !opID !38, !opSignedness !4
  %"36." = load i32, i32* %"4.i", align 4, !opID !39, !opSignedness !4
  %"37.idxprom9" = sext i32 %"36." to i64, !opID !40, !opSignedness !4
  %"38.arrayidx10" = getelementptr inbounds i32, i32* %"35.", i64 %"37.idxprom9", !opID !41, !opSignedness !4
  store i32 %"34.", i32* %"38.arrayidx10", align 4, !opID !42, !opSignedness !4
  br label %for.inc, !opID !43, !opSignedness !4

for.inc:                                          ; preds = %for.body
  %"41." = load i32, i32* %"4.i", align 4, !opID !44, !opSignedness !4
  %"42.inc" = add nsw i32 %"41.", 1, !opID !45, !opSignedness !4
  store i32 %"42.inc", i32* %"4.i", align 4, !opID !46, !opSignedness !4
  br label %for.cond, !opID !47, !opSignedness !4

for.end:                                          ; preds = %for.cond
  ret void, !opID !48, !opSignedness !4
}

; Function Attrs: noinline norecurse optnone uwtable
define dso_local i32 @main(i32 %argc, i8** %argv) #1 {
entry:
  %"46.retval" = alloca i32, align 4, !opID !49, !opSignedness !4
  %"47.argc.addr" = alloca i32, align 4, !opID !50, !opSignedness !4
  %"48.argv.addr" = alloca i8**, align 8, !opID !51, !opSignedness !4
  %"49.indata" = alloca [8000 x i32], align 16, !opID !52, !opSignedness !4
  %"50.outdata" = alloca [8000 x i32], align 16, !opID !53, !opSignedness !4
  store i32 0, i32* %"46.retval", align 4, !opID !54, !opSignedness !4
  store i32 %argc, i32* %"47.argc.addr", align 4, !opID !55, !opSignedness !4
  store i8** %argv, i8*** %"48.argv.addr", align 8, !opID !56, !opSignedness !4
  %"54.arraydecay" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"49.indata", i32 0, i32 0, !opID !57, !opSignedness !4
  %"55." = load i8**, i8*** %"48.argv.addr", align 8, !opID !58, !opSignedness !4
  %"56.arrayidx" = getelementptr inbounds i8*, i8** %"55.", i64 1, !opID !59, !opSignedness !4
  %"57." = load i8*, i8** %"56.arrayidx", align 8, !opID !60, !opSignedness !4
  call void @_Z13populateInputPiiPKc(i32* %"54.arraydecay", i32 8000, i8* %"57."), !opID !61, !opSignedness !4
  %"59.arraydecay1" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"49.indata", i32 0, i32 0, !opID !62, !opSignedness !4
  %"60.arraydecay2" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"50.outdata", i32 0, i32 0, !opID !63, !opSignedness !4
  call void @_Z7examplePiS_(i32* %"59.arraydecay1", i32* %"60.arraydecay2"), !opID !64, !opSignedness !4
  %"62.arraydecay3" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"50.outdata", i32 0, i32 0, !opID !65, !opSignedness !4
  %"63." = load i8**, i8*** %"48.argv.addr", align 8, !opID !66, !opSignedness !4
  %"64.arrayidx4" = getelementptr inbounds i8*, i8** %"63.", i64 2, !opID !67, !opSignedness !4
  %"65." = load i8*, i8** %"64.arrayidx4", align 8, !opID !68, !opSignedness !4
  call void @_Z14populateOutputPiiPKc(i32* %"62.arraydecay3", i32 8000, i8* %"65."), !opID !69, !opSignedness !4
  ret i32 0, !opID !2, !opSignedness !4
}

declare dso_local void @_Z13populateInputPiiPKc(i32*, i32, i8*) #2

declare dso_local void @_Z14populateOutputPiiPKc(i32*, i32, i8*) #2

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline norecurse optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}
!OP-ID-COUNTER = !{!2}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 7.0.0 (tags/RELEASE_700/final)"}
!2 = !{i64 67}
!3 = !{i64 1}
!4 = !{!"unknownSignedness"}
!5 = !{i64 2}
!6 = !{i64 3}
!7 = !{i64 4}
!8 = !{i64 5}
!9 = !{i64 6}
!10 = !{i64 7}
!11 = !{i64 8}
!12 = !{i64 9}
!13 = !{i64 10}
!14 = !{i64 11}
!15 = !{i64 12}
!16 = !{i64 13}
!17 = !{i64 14}
!18 = !{i64 15}
!19 = !{i64 16}
!20 = !{i64 17}
!21 = !{i64 18}
!22 = !{i64 19}
!23 = !{i64 20}
!24 = !{i64 21}
!25 = !{i64 22}
!26 = !{i64 23}
!27 = !{i64 24}
!28 = !{i64 25}
!29 = !{i64 26}
!30 = !{i64 27}
!31 = !{i64 28}
!32 = !{i64 29}
!33 = !{i64 30}
!34 = !{i64 31}
!35 = !{i64 32}
!36 = !{i64 33}
!37 = !{i64 34}
!38 = !{i64 35}
!39 = !{i64 36}
!40 = !{i64 37}
!41 = !{i64 38}
!42 = !{i64 39}
!43 = !{i64 40}
!44 = !{i64 41}
!45 = !{i64 42}
!46 = !{i64 43}
!47 = !{i64 44}
!48 = !{i64 45}
!49 = !{i64 46}
!50 = !{i64 47}
!51 = !{i64 48}
!52 = !{i64 49}
!53 = !{i64 50}
!54 = !{i64 51}
!55 = !{i64 52}
!56 = !{i64 53}
!57 = !{i64 54}
!58 = !{i64 55}
!59 = !{i64 56}
!60 = !{i64 57}
!61 = !{i64 58}
!62 = !{i64 59}
!63 = !{i64 60}
!64 = !{i64 61}
!65 = !{i64 62}
!66 = !{i64 63}
!67 = !{i64 64}
!68 = !{i64 65}
!69 = !{i64 66}
