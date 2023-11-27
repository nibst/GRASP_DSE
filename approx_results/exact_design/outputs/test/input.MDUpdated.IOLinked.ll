; ModuleID = 'input.MDUpdated.IOLinked.bc'
source_filename = "llvm-link"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i64, i16, i8, [1 x i8], i8*, i64, %struct._IO_codecvt*, %struct._IO_wide_data*, %struct._IO_FILE*, i8*, i64, i32, [20 x i8] }
%struct._IO_marker = type opaque
%struct._IO_codecvt = type opaque
%struct._IO_wide_data = type opaque

@test_data = dso_local global [8000 x i32] zeroinitializer, align 16
@result = dso_local global [8000 x i32] zeroinitializer, align 16
@.str = private unnamed_addr constant [2 x i8] c"r\00", align 1
@.str.1 = private unnamed_addr constant [3 x i8] c"%i\00", align 1
@stderr = external dso_local global %struct._IO_FILE*, align 8
@.str.2 = private unnamed_addr constant [11 x i8] c"input good\00", align 1
@.str.3 = private unnamed_addr constant [2 x i8] c"w\00", align 1
@.str.4 = private unnamed_addr constant [4 x i8] c"%i\0A\00", align 1
@.str.5 = private unnamed_addr constant [2 x i8] c"r\00", align 1
@.str.1.6 = private unnamed_addr constant [3 x i8] c"%i\00", align 1
@.str.2.7 = private unnamed_addr constant [2 x i8] c"w\00", align 1
@.str.3.8 = private unnamed_addr constant [4 x i8] c"%i\0A\00", align 1

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

; Function Attrs: noinline optnone uwtable
define dso_local void @_Z13populateInputPiiPKc(i32* %inputVector, i32 %numElts, i8* %fileName) #1 {
entry:
  %"46.inputVector.addr" = alloca i32*, align 8, !opID !49, !opSignedness !4
  %"47.numElts.addr" = alloca i32, align 4, !opID !50, !opSignedness !4
  %"48.fileName.addr" = alloca i8*, align 8, !opID !51, !opSignedness !4
  %"49.inputFile" = alloca %struct._IO_FILE*, align 8, !opID !52, !opSignedness !4
  %"50.i" = alloca i32, align 4, !opID !53, !opSignedness !4
  store i32* %inputVector, i32** %"46.inputVector.addr", align 8, !opID !54, !opSignedness !4
  store i32 %numElts, i32* %"47.numElts.addr", align 4, !opID !55, !opSignedness !4
  store i8* %fileName, i8** %"48.fileName.addr", align 8, !opID !56, !opSignedness !4
  %"54." = load i8*, i8** %"48.fileName.addr", align 8, !opID !57, !opSignedness !4
  %"55.call" = call noalias %struct._IO_FILE* @fopen(i8* %"54.", i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str, i32 0, i32 0)), !opID !58, !opSignedness !4
  store %struct._IO_FILE* %"55.call", %struct._IO_FILE** %"49.inputFile", align 8, !opID !59, !opSignedness !4
  store i32 0, i32* %"50.i", align 4, !opID !60, !opSignedness !4
  br label %for.cond, !opID !61, !opSignedness !4

for.cond:                                         ; preds = %for.inc, %entry
  %"59." = load i32, i32* %"50.i", align 4, !opID !62, !opSignedness !4
  %"60." = load i32, i32* %"47.numElts.addr", align 4, !opID !63, !opSignedness !4
  %"61.cmp" = icmp slt i32 %"59.", %"60.", !opID !64, !opSignedness !4
  br i1 %"61.cmp", label %for.body, label %for.end, !opID !65, !opSignedness !4

for.body:                                         ; preds = %for.cond
  %"63." = load %struct._IO_FILE*, %struct._IO_FILE** %"49.inputFile", align 8, !opID !66, !opSignedness !4
  %"64." = load i32*, i32** %"46.inputVector.addr", align 8, !opID !67, !opSignedness !4
  %"65." = load i32, i32* %"50.i", align 4, !opID !68, !opSignedness !4
  %"66.idxprom" = sext i32 %"65." to i64, !opID !69, !opSignedness !4
  %"67.arrayidx" = getelementptr inbounds i32, i32* %"64.", i64 %"66.idxprom", !opID !70, !opSignedness !4
  %"68.call1" = call i32 (%struct._IO_FILE*, i8*, ...) @__isoc99_fscanf(%struct._IO_FILE* %"63.", i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.1, i32 0, i32 0), i32* %"67.arrayidx"), !opID !71, !opSignedness !4
  br label %for.inc, !opID !72, !opSignedness !4

for.inc:                                          ; preds = %for.body
  %"70." = load i32, i32* %"50.i", align 4, !opID !73, !opSignedness !4
  %"71.inc" = add nsw i32 %"70.", 1, !opID !74, !opSignedness !4
  store i32 %"71.inc", i32* %"50.i", align 4, !opID !75, !opSignedness !4
  br label %for.cond, !opID !76, !opSignedness !4

for.end:                                          ; preds = %for.cond
  %"74." = load %struct._IO_FILE*, %struct._IO_FILE** @stderr, align 8, !opID !77, !opSignedness !4
  %"75.call2" = call i32 (%struct._IO_FILE*, i8*, ...) @fprintf(%struct._IO_FILE* %"74.", i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.2, i32 0, i32 0)), !opID !78, !opSignedness !4
  %"76." = load %struct._IO_FILE*, %struct._IO_FILE** %"49.inputFile", align 8, !opID !79, !opSignedness !4
  %"77.call3" = call i32 @fclose(%struct._IO_FILE* %"76."), !opID !80, !opSignedness !4
  ret void, !opID !81, !opSignedness !4
}

declare dso_local noalias %struct._IO_FILE* @fopen(i8*, i8*) #2

declare dso_local i32 @__isoc99_fscanf(%struct._IO_FILE*, i8*, ...) #2

declare dso_local i32 @fprintf(%struct._IO_FILE*, i8*, ...) #2

declare dso_local i32 @fclose(%struct._IO_FILE*) #2

; Function Attrs: noinline optnone uwtable
define dso_local void @_Z14populateOutputPiiPKc(i32* %outputVector, i32 %numElts, i8* %fileName) #1 {
entry:
  %"79.outputVector.addr" = alloca i32*, align 8, !opID !82, !opSignedness !4
  %"80.numElts.addr" = alloca i32, align 4, !opID !83, !opSignedness !4
  %"81.fileName.addr" = alloca i8*, align 8, !opID !84, !opSignedness !4
  %"82.outputFile" = alloca %struct._IO_FILE*, align 8, !opID !85, !opSignedness !4
  %"83.i" = alloca i32, align 4, !opID !86, !opSignedness !4
  store i32* %outputVector, i32** %"79.outputVector.addr", align 8, !opID !87, !opSignedness !4
  store i32 %numElts, i32* %"80.numElts.addr", align 4, !opID !88, !opSignedness !4
  store i8* %fileName, i8** %"81.fileName.addr", align 8, !opID !89, !opSignedness !4
  %"87." = load i8*, i8** %"81.fileName.addr", align 8, !opID !90, !opSignedness !4
  %"88.call" = call noalias %struct._IO_FILE* @fopen(i8* %"87.", i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.3, i32 0, i32 0)), !opID !91, !opSignedness !4
  store %struct._IO_FILE* %"88.call", %struct._IO_FILE** %"82.outputFile", align 8, !opID !92, !opSignedness !4
  store i32 0, i32* %"83.i", align 4, !opID !93, !opSignedness !4
  br label %for.cond, !opID !94, !opSignedness !4

for.cond:                                         ; preds = %for.inc, %entry
  %"92." = load i32, i32* %"83.i", align 4, !opID !95, !opSignedness !4
  %"93." = load i32, i32* %"80.numElts.addr", align 4, !opID !96, !opSignedness !4
  %"94.cmp" = icmp slt i32 %"92.", %"93.", !opID !97, !opSignedness !4
  br i1 %"94.cmp", label %for.body, label %for.end, !opID !98, !opSignedness !4

for.body:                                         ; preds = %for.cond
  %"96." = load %struct._IO_FILE*, %struct._IO_FILE** %"82.outputFile", align 8, !opID !99, !opSignedness !4
  %"97." = load i32*, i32** %"79.outputVector.addr", align 8, !opID !100, !opSignedness !4
  %"98." = load i32, i32* %"83.i", align 4, !opID !101, !opSignedness !4
  %"99.idxprom" = sext i32 %"98." to i64, !opID !102, !opSignedness !4
  %"100.arrayidx" = getelementptr inbounds i32, i32* %"97.", i64 %"99.idxprom", !opID !103, !opSignedness !4
  %"101." = load i32, i32* %"100.arrayidx", align 4, !opID !104, !opSignedness !4
  %"102.call1" = call i32 (%struct._IO_FILE*, i8*, ...) @fprintf(%struct._IO_FILE* %"96.", i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.4, i32 0, i32 0), i32 %"101."), !opID !105, !opSignedness !4
  br label %for.inc, !opID !106, !opSignedness !4

for.inc:                                          ; preds = %for.body
  %"104." = load i32, i32* %"83.i", align 4, !opID !107, !opSignedness !4
  %"105.inc" = add nsw i32 %"104.", 1, !opID !108, !opSignedness !4
  store i32 %"105.inc", i32* %"83.i", align 4, !opID !109, !opSignedness !4
  br label %for.cond, !opID !110, !opSignedness !4

for.end:                                          ; preds = %for.cond
  %"108." = load %struct._IO_FILE*, %struct._IO_FILE** %"82.outputFile", align 8, !opID !111, !opSignedness !4
  %"109.call2" = call i32 @fclose(%struct._IO_FILE* %"108."), !opID !112, !opSignedness !4
  ret void, !opID !113, !opSignedness !4
}

; Function Attrs: noinline norecurse optnone uwtable
define dso_local i32 @main(i32 %argc, i8** %argv) #3 {
entry:
  %"111.retval" = alloca i32, align 4, !opID !114, !opSignedness !4
  %"112.argc.addr" = alloca i32, align 4, !opID !115, !opSignedness !4
  %"113.argv.addr" = alloca i8**, align 8, !opID !116, !opSignedness !4
  %"114.indata" = alloca [8000 x i32], align 16, !opID !117, !opSignedness !4
  %"115.outdata" = alloca [8000 x i32], align 16, !opID !118, !opSignedness !4
  store i32 0, i32* %"111.retval", align 4, !opID !119, !opSignedness !4
  store i32 %argc, i32* %"112.argc.addr", align 4, !opID !120, !opSignedness !4
  store i8** %argv, i8*** %"113.argv.addr", align 8, !opID !121, !opSignedness !4
  %"119.arraydecay" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"114.indata", i32 0, i32 0, !opID !122, !opSignedness !4
  %"120." = load i8**, i8*** %"113.argv.addr", align 8, !opID !123, !opSignedness !4
  %"121.arrayidx" = getelementptr inbounds i8*, i8** %"120.", i64 1, !opID !124, !opSignedness !4
  %"122." = load i8*, i8** %"121.arrayidx", align 8, !opID !125, !opSignedness !4
  call void @_Z13populateInputPiiPKc(i32* %"119.arraydecay", i32 8000, i8* %"122."), !opID !126, !opSignedness !4
  %"124.arraydecay1" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"114.indata", i32 0, i32 0, !opID !127, !opSignedness !4
  %"125.arraydecay2" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"115.outdata", i32 0, i32 0, !opID !128, !opSignedness !4
  call void @_Z7examplePiS_(i32* %"124.arraydecay1", i32* %"125.arraydecay2"), !opID !129, !opSignedness !4
  %"127.arraydecay3" = getelementptr inbounds [8000 x i32], [8000 x i32]* %"115.outdata", i32 0, i32 0, !opID !130, !opSignedness !4
  %"128." = load i8**, i8*** %"113.argv.addr", align 8, !opID !131, !opSignedness !4
  %"129.arrayidx4" = getelementptr inbounds i8*, i8** %"128.", i64 2, !opID !132, !opSignedness !4
  %"130." = load i8*, i8** %"129.arrayidx4", align 8, !opID !133, !opSignedness !4
  call void @_Z14populateOutputPiiPKc(i32* %"127.arraydecay3", i32 8000, i8* %"130."), !opID !134, !opSignedness !4
  ret i32 0, !opID !1, !opSignedness !4
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @populateInput(i32* %inputVector, i32 %numElts, i8* %fileName) #0 {
entry:
  %inputVector.addr = alloca i32*, align 8
  %numElts.addr = alloca i32, align 4
  %fileName.addr = alloca i8*, align 8
  %inputFile = alloca %struct._IO_FILE*, align 8
  %i = alloca i32, align 4
  store i32* %inputVector, i32** %inputVector.addr, align 8
  store i32 %numElts, i32* %numElts.addr, align 4
  store i8* %fileName, i8** %fileName.addr, align 8
  %0 = load i8*, i8** %fileName.addr, align 8
  %call = call noalias %struct._IO_FILE* @fopen(i8* %0, i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.5, i32 0, i32 0))
  store %struct._IO_FILE* %call, %struct._IO_FILE** %inputFile, align 8
  store i32 0, i32* %i, align 4
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %entry
  %1 = load i32, i32* %i, align 4
  %2 = load i32, i32* %numElts.addr, align 4
  %cmp = icmp slt i32 %1, %2
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %3 = load %struct._IO_FILE*, %struct._IO_FILE** %inputFile, align 8
  %4 = load i32*, i32** %inputVector.addr, align 8
  %5 = load i32, i32* %i, align 4
  %idxprom = sext i32 %5 to i64
  %arrayidx = getelementptr inbounds i32, i32* %4, i64 %idxprom
  %call1 = call i32 (%struct._IO_FILE*, i8*, ...) @__isoc99_fscanf(%struct._IO_FILE* %3, i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.1.6, i32 0, i32 0), i32* %arrayidx)
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %6 = load i32, i32* %i, align 4
  %inc = add nsw i32 %6, 1
  store i32 %inc, i32* %i, align 4
  br label %for.cond

for.end:                                          ; preds = %for.cond
  %7 = load %struct._IO_FILE*, %struct._IO_FILE** %inputFile, align 8
  %call2 = call i32 @fclose(%struct._IO_FILE* %7)
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @populateOutput(i32* %outputVector, i32 %numElts, i8* %fileName) #0 {
entry:
  %outputVector.addr = alloca i32*, align 8
  %numElts.addr = alloca i32, align 4
  %fileName.addr = alloca i8*, align 8
  %outputFile = alloca %struct._IO_FILE*, align 8
  %i = alloca i32, align 4
  store i32* %outputVector, i32** %outputVector.addr, align 8
  store i32 %numElts, i32* %numElts.addr, align 4
  store i8* %fileName, i8** %fileName.addr, align 8
  %0 = load i8*, i8** %fileName.addr, align 8
  %call = call noalias %struct._IO_FILE* @fopen(i8* %0, i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.2.7, i32 0, i32 0))
  store %struct._IO_FILE* %call, %struct._IO_FILE** %outputFile, align 8
  store i32 0, i32* %i, align 4
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %entry
  %1 = load i32, i32* %i, align 4
  %2 = load i32, i32* %numElts.addr, align 4
  %cmp = icmp slt i32 %1, %2
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %3 = load %struct._IO_FILE*, %struct._IO_FILE** %outputFile, align 8
  %4 = load i32*, i32** %outputVector.addr, align 8
  %5 = load i32, i32* %i, align 4
  %idxprom = sext i32 %5 to i64
  %arrayidx = getelementptr inbounds i32, i32* %4, i64 %idxprom
  %6 = load i32, i32* %arrayidx, align 4
  %call1 = call i32 (%struct._IO_FILE*, i8*, ...) @fprintf(%struct._IO_FILE* %3, i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.3.8, i32 0, i32 0), i32 %6)
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %7 = load i32, i32* %i, align 4
  %inc = add nsw i32 %7, 1
  store i32 %inc, i32* %i, align 4
  br label %for.cond

for.end:                                          ; preds = %for.cond
  %8 = load %struct._IO_FILE*, %struct._IO_FILE** %outputFile, align 8
  %call2 = call i32 @fclose(%struct._IO_FILE* %8)
  ret void
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { noinline norecurse optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0, !0}
!OP-ID-COUNTER = !{!1}
!llvm.module.flags = !{!2}

!0 = !{!"clang version 7.0.0 (tags/RELEASE_700/final)"}
!1 = !{i64 132}
!2 = !{i32 1, !"wchar_size", i32 4}
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
!70 = !{i64 67}
!71 = !{i64 68}
!72 = !{i64 69}
!73 = !{i64 70}
!74 = !{i64 71}
!75 = !{i64 72}
!76 = !{i64 73}
!77 = !{i64 74}
!78 = !{i64 75}
!79 = !{i64 76}
!80 = !{i64 77}
!81 = !{i64 78}
!82 = !{i64 79}
!83 = !{i64 80}
!84 = !{i64 81}
!85 = !{i64 82}
!86 = !{i64 83}
!87 = !{i64 84}
!88 = !{i64 85}
!89 = !{i64 86}
!90 = !{i64 87}
!91 = !{i64 88}
!92 = !{i64 89}
!93 = !{i64 90}
!94 = !{i64 91}
!95 = !{i64 92}
!96 = !{i64 93}
!97 = !{i64 94}
!98 = !{i64 95}
!99 = !{i64 96}
!100 = !{i64 97}
!101 = !{i64 98}
!102 = !{i64 99}
!103 = !{i64 100}
!104 = !{i64 101}
!105 = !{i64 102}
!106 = !{i64 103}
!107 = !{i64 104}
!108 = !{i64 105}
!109 = !{i64 106}
!110 = !{i64 107}
!111 = !{i64 108}
!112 = !{i64 109}
!113 = !{i64 110}
!114 = !{i64 111}
!115 = !{i64 112}
!116 = !{i64 113}
!117 = !{i64 114}
!118 = !{i64 115}
!119 = !{i64 116}
!120 = !{i64 117}
!121 = !{i64 118}
!122 = !{i64 119}
!123 = !{i64 120}
!124 = !{i64 121}
!125 = !{i64 122}
!126 = !{i64 123}
!127 = !{i64 124}
!128 = !{i64 125}
!129 = !{i64 126}
!130 = !{i64 127}
!131 = !{i64 128}
!132 = !{i64 129}
!133 = !{i64 130}
!134 = !{i64 131}
