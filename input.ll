; ModuleID = '../input.bc'
source_filename = "./benchmark_testing/input.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
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

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_Z7examplePiS_(i32* %a, i32* %b) #0 {
entry:
  %a.addr = alloca i32*, align 8
  %b.addr = alloca i32*, align 8
  %buff = alloca [8000 x i32], align 16
  %i = alloca i32, align 4
  store i32* %a, i32** %a.addr, align 8
  store i32* %b, i32** %b.addr, align 8
  br label %example_label0

example_label0:                                   ; preds = %entry
  store i32 0, i32* %i, align 4
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %example_label0
  %0 = load i32, i32* %i, align 4
  %cmp = icmp slt i32 %0, 8000
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %1 = load i32*, i32** %a.addr, align 8
  %2 = load i32, i32* %i, align 4
  %idxprom = sext i32 %2 to i64
  %arrayidx = getelementptr inbounds i32, i32* %1, i64 %idxprom
  %3 = load i32, i32* %arrayidx, align 4
  %4 = load i32, i32* %i, align 4
  %idxprom1 = sext i32 %4 to i64
  %arrayidx2 = getelementptr inbounds [8000 x i32], [8000 x i32]* %buff, i64 0, i64 %idxprom1
  store i32 %3, i32* %arrayidx2, align 4
  %5 = load i32, i32* %i, align 4
  %idxprom3 = sext i32 %5 to i64
  %arrayidx4 = getelementptr inbounds [8000 x i32], [8000 x i32]* %buff, i64 0, i64 %idxprom3
  %6 = load i32, i32* %arrayidx4, align 4
  %add = add nsw i32 %6, 100
  %7 = load i32, i32* %i, align 4
  %idxprom5 = sext i32 %7 to i64
  %arrayidx6 = getelementptr inbounds [8000 x i32], [8000 x i32]* %buff, i64 0, i64 %idxprom5
  store i32 %add, i32* %arrayidx6, align 4
  %8 = load i32, i32* %i, align 4
  %idxprom7 = sext i32 %8 to i64
  %arrayidx8 = getelementptr inbounds [8000 x i32], [8000 x i32]* %buff, i64 0, i64 %idxprom7
  %9 = load i32, i32* %arrayidx8, align 4
  %10 = load i32*, i32** %b.addr, align 8
  %11 = load i32, i32* %i, align 4
  %idxprom9 = sext i32 %11 to i64
  %arrayidx10 = getelementptr inbounds i32, i32* %10, i64 %idxprom9
  store i32 %9, i32* %arrayidx10, align 4
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %12 = load i32, i32* %i, align 4
  %inc = add nsw i32 %12, 1
  store i32 %inc, i32* %i, align 4
  br label %for.cond

for.end:                                          ; preds = %for.cond
  ret void
}

; Function Attrs: noinline optnone uwtable
define dso_local void @_Z13populateInputPiiPKc(i32* %inputVector, i32 %numElts, i8* %fileName) #1 {
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
  %call = call noalias %struct._IO_FILE* @fopen(i8* %0, i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str, i32 0, i32 0))
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
  %call1 = call i32 (%struct._IO_FILE*, i8*, ...) @__isoc99_fscanf(%struct._IO_FILE* %3, i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.1, i32 0, i32 0), i32* %arrayidx)
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %6 = load i32, i32* %i, align 4
  %inc = add nsw i32 %6, 1
  store i32 %inc, i32* %i, align 4
  br label %for.cond

for.end:                                          ; preds = %for.cond
  %7 = load %struct._IO_FILE*, %struct._IO_FILE** @stderr, align 8
  %call2 = call i32 (%struct._IO_FILE*, i8*, ...) @fprintf(%struct._IO_FILE* %7, i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.2, i32 0, i32 0))
  %8 = load %struct._IO_FILE*, %struct._IO_FILE** %inputFile, align 8
  %call3 = call i32 @fclose(%struct._IO_FILE* %8)
  ret void
}

declare dso_local noalias %struct._IO_FILE* @fopen(i8*, i8*) #2

declare dso_local i32 @__isoc99_fscanf(%struct._IO_FILE*, i8*, ...) #2

declare dso_local i32 @fprintf(%struct._IO_FILE*, i8*, ...) #2

declare dso_local i32 @fclose(%struct._IO_FILE*) #2

; Function Attrs: noinline optnone uwtable
define dso_local void @_Z14populateOutputPiiPKc(i32* %outputVector, i32 %numElts, i8* %fileName) #1 {
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
  %call = call noalias %struct._IO_FILE* @fopen(i8* %0, i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.3, i32 0, i32 0))
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
  %call1 = call i32 (%struct._IO_FILE*, i8*, ...) @fprintf(%struct._IO_FILE* %3, i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.4, i32 0, i32 0), i32 %6)
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

; Function Attrs: noinline norecurse optnone uwtable
define dso_local i32 @main(i32 %argc, i8** %argv) #3 {
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
  call void @_Z13populateInputPiiPKc(i32* %arraydecay, i32 8000, i8* %1)
  %arraydecay1 = getelementptr inbounds [8000 x i32], [8000 x i32]* %indata, i32 0, i32 0
  %arraydecay2 = getelementptr inbounds [8000 x i32], [8000 x i32]* %outdata, i32 0, i32 0
  call void @_Z7examplePiS_(i32* %arraydecay1, i32* %arraydecay2)
  %arraydecay3 = getelementptr inbounds [8000 x i32], [8000 x i32]* %outdata, i32 0, i32 0
  %2 = load i8**, i8*** %argv.addr, align 8
  %arrayidx4 = getelementptr inbounds i8*, i8** %2, i64 2
  %3 = load i8*, i8** %arrayidx4, align 8
  call void @_Z14populateOutputPiiPKc(i32* %arraydecay3, i32 8000, i8* %3)
  ret i32 0
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { noinline norecurse optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 7.0.0 (tags/RELEASE_700/final)"}
