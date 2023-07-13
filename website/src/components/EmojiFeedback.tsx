import { SubmitHandler, useForm } from "react-hook-form";

type EmojiFeedbackProps = {
  zoneName: string;
  userID: string;
};

export default function({ zoneName, userID }: EmojiFeedbackProps) {
  type Option = { label: string; value: string };

  // TODO: Could swap this to ZOD. Just need to set the resolver in useForm
  type Inputs = {
    emojiFeedback: Option;
    thoughts: string;
    improvements: string;
  };

  const OPTIONS: Array<Option> = [
    { label: "😠", value: "awful" },
    { label: "☹️", value: "bad" },
    { label: "😐", value: "average" },
    { label: "🙂", value: "good" },
    { label: "😃", value: "amazing" },
  ];

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Inputs>();
  // TODO: Plug this into API
  const onSubmit: SubmitHandler<Inputs> = (data) => console.log(`${userID} gave this feedback: `, data);

  if (errors) {
    console.log("Errors: ", errors);
  }

  return (
    <div className="self-center">
      <h1 className="text-3xl font-bold">Tell us how we did!</h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="text-8xl select-none pt-5 pb-5">
          <ul className="inline-flex w-4/5 justify-between">
            {OPTIONS.map((option) => (
              <li key={option.value}>
                <input
                  id={option.value}
                  {...register("emojiFeedback", { required: true })}
                  type="radio"
                  value={option.value}
                  className="hidden peer"
                />
                <label
                  key={option.label}
                  htmlFor={option.value}
                  className="grayscale hover:grayscale-0 peer-checked:grayscale-0 cursor-pointer"
                >
                  {option.label}
                </label>
              </li>
            ))}
          </ul>
        </div>

        <div className="pb-5">
          <label htmlFor="thoughts" className="font-bold">
            Please let us know what you thought was good about {zoneName}:
          </label>
          <input
            id="thoughts"
            type="text"
            className="block w-full border p-2"
            {...register("thoughts", { required: true, min: 5 })}
          />
        </div>

        <div className="pb-5">
          <label htmlFor="improvements" className="font-bold">
            Please let us know what you thought could have improved {zoneName}:
          </label>
          <input
            id="improvements"
            type="text"
            className="block w-full border p-2"
            {...register("improvements", { required: true, min: 5 })}
          />
        </div>

        <button
          type="submit"
          className="block cursor-pointer border border-black p-2 rounded"
        >
          Submit
        </button>
      </form>
    </div>
  );
}
