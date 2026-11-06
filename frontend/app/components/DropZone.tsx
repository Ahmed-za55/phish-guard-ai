"use client";

import { DragEvent } from "react";

type Props = {
  kind: "image" | "email";
  file: File | null;
  preview: string | null;
  onFile: (file: File) => void;
  onInvalid: (message: string) => void;
  onRemove: () => void;
};

const COPY = {
  image: {
    title: "Drop a screenshot here",
    hint: "PNG, JPG or WEBP",
    accept: "image/png,image/jpeg,image/webp",
    invalid: "Please choose a PNG, JPG or WEBP image.",
  },
  email: {
    title: "Drop an .eml file here",
    hint: "Export the message from your mail app as .eml",
    accept: ".eml,message/rfc822",
    invalid: "Please choose an .eml email file.",
  },
};

export default function DropZone({ kind, file, preview, onFile, onInvalid, onRemove }: Props) {
  const copy = COPY[kind];

  function accept(candidate: File | null | undefined) {
    if (!candidate) return;
    const valid =
      kind === "image"
        ? candidate.type.startsWith("image/")
        : candidate.name.toLowerCase().endsWith(".eml");
    if (!valid) {
      onInvalid(copy.invalid);
      return;
    }
    onFile(candidate);
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    accept(event.dataTransfer.files?.[0]);
  }

  return (
    <div>
      <label
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
        className="flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-line bg-paper px-6 py-12 text-center transition-colors hover:border-accent focus-within:border-accent focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-accent"
      >
        {preview ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={preview} alt="Selected screenshot" className="max-h-72 rounded-md object-contain" />
        ) : (
          <>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" aria-hidden className="text-ink-2">
              <path d="M12 16V5m0 0-4 4m4-4 4 4M5 15v3a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-3" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <span className="mt-3 text-lg font-semibold">{copy.title}</span>
            <span className="mt-1 text-ink-2">or click to choose a file</span>
            <span className="mt-2 text-sm text-ink-2">{copy.hint}</span>
          </>
        )}
        <input
          type="file"
          accept={copy.accept}
          className="sr-only"
          onChange={(e) => {
            accept(e.target.files?.[0]);
            e.target.value = "";
          }}
        />
      </label>

      {file && (
        <div className="mt-3 flex items-center justify-between gap-4 rounded-md border border-line bg-card px-4 py-3">
          <div className="min-w-0">
            <p className="truncate font-medium">{file.name}</p>
            <p className="text-sm text-ink-2">{(file.size / 1024).toFixed(1)} KB</p>
          </div>
          <button
            type="button"
            onClick={onRemove}
            className="shrink-0 rounded-md px-3 py-2 text-sm font-medium text-ink-2 hover:bg-paper hover:text-ink"
          >
            Remove
          </button>
        </div>
      )}
    </div>
  );
}
